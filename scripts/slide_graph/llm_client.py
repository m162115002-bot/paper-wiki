"""Gemini API structured output client with Free-Tier 429 pacing, auto-retry & fallback."""
from __future__ import annotations

import os
import re
import threading
import time
from typing import Any, List, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

DEFAULT_FALLBACK_MODELS: List[str] = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
]

_PACE_LOCK = threading.Lock()
_LAST_CALL_TS = 0.0
_MIN_INTERVAL_SEC = float(os.environ.get("GEMINI_MIN_INTERVAL_SEC", "6.0"))


def _extract_retry_seconds(err_msg: str, default_sec: float = 15.0) -> float:
    m = re.search(r"retry in\s+([0-9]+(?:\.[0-9]+)?)s", err_msg, flags=re.IGNORECASE)
    if m:
        return min(90.0, float(m.group(1)) + 2.0)
    m2 = re.search(r"retryDelay['\"]?:\s*['\"]?(\d+)s", err_msg, flags=re.IGNORECASE)
    if m2:
        return min(90.0, float(m2.group(1)) + 2.0)
    return default_sec


def _pace_request() -> None:
    global _LAST_CALL_TS
    with _PACE_LOCK:
        now = time.monotonic()
        elapsed = now - _LAST_CALL_TS
        if _LAST_CALL_TS > 0 and elapsed < _MIN_INTERVAL_SEC:
            time.sleep(_MIN_INTERVAL_SEC - elapsed)
        _LAST_CALL_TS = time.monotonic()


class GeminiStructuredClient:
    """Thin wrapper around google-genai supporting text & PDF inputs with 429/503 retry."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
        self._client = None

    def _get_client(self):
        if self._client is None:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "找不到環境變數 GEMINI_API_KEY，請先執行：\n"
                    '  $env:GEMINI_API_KEY="你的金鑰"'
                )
            from google import genai

            self._client = genai.Client(api_key=api_key)
        return self._client

    def _build_model_chain(self) -> List[str]:
        chain = [self.model]
        for m in DEFAULT_FALLBACK_MODELS:
            if m not in chain:
                chain.append(m)
        return chain

    def generate_structured(
        self,
        system_instruction: str,
        prompt: str,
        schema: Type[T],
        temperature: float = 0.3,
        max_rounds: int = 3,
        pdf_bytes: bytes | None = None,
    ) -> T:
        from google.genai import types

        client = self._get_client()
        models = self._build_model_chain()
        last_err: Exception | None = None

        contents: Any = (
            [types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"), prompt]
            if pdf_bytes is not None
            else prompt
        )

        for round_idx in range(1, max_rounds + 1):
            for m in models:
                _pace_request()
                print(
                    f"[Gemini] 第 {round_idx} 輪呼叫模型 {m}（輸出 {schema.__name__}）...",
                    flush=True,
                )
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            response_mime_type="application/json",
                            response_schema=schema,
                            temperature=temperature,
                        ),
                    )
                    print(f"[Gemini] 模型 {m} 回傳成功！", flush=True)
                    return schema.model_validate_json(response.text)
                except Exception as exc:
                    last_err = exc
                    msg = str(exc)
                    is_rate_limit = "429" in msg or "RESOURCE_EXHAUSTED" in msg
                    is_server_busy = any(
                        code in msg
                        for code in ("503", "UNAVAILABLE", "500", "DEADLINE_EXCEEDED")
                    )
                    if is_rate_limit:
                        if m != models[-1]:
                            print(
                                f"[Gemini] 模型 {m} 達免費版每分鐘上限（429），立即切換備援模型...",
                                flush=True,
                            )
                            continue
                        wait_sec = _extract_retry_seconds(msg, default_sec=60.0)
                        print(
                            f"[Gemini] 本輪模型皆達免費版速率上限（429），自動等待 {wait_sec:.0f} 秒後繼續...",
                            flush=True,
                        )
                        time.sleep(wait_sec)
                        continue
                    if is_server_busy:
                        wait_sec = 5 * round_idx
                        print(
                            f"[Gemini] 模型 {m} 暫時塞車（503），等待 {wait_sec} 秒後切換備援模型...",
                            flush=True,
                        )
                        time.sleep(wait_sec)
                        continue
                    raise

        raise RuntimeError(f"所有備援模型重試後仍失敗，最後錯誤：{last_err}") from last_err
