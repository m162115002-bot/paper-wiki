# Slide Graph v3 — PDF 一條龍自動化投影片管線

整合四步驟流程：**放 PDF → 自動匯入 Wiki 與擷取 PDF 關鍵圖表 → 確認大綱 → 製作並驗收單檔粉彩 HTML 簡報**。

## 首次升級安裝（補裝圖表裁切套件）
```powershell
cd paper-wiki\scripts\slide_graph
pip install -r requirements.txt
```

## 日常 4 步驟使用方式
1. 把原始 PDF 放進 `paper-wiki\raw\papers\`。
2. 啟動 `.venv` 與 API Key 後，執行 `start`（會自動偵測新 PDF、擷取關鍵圖表至 `raw/assets/`、寫入 `wiki/` 並產出大綱停在 HITL 1）：
   ```powershell
   python run.py start --pdf "raw\papers\你的檔名.pdf" --topic "報告主題" --presenter "黃少杰" --course "健康心理學" --date "2026/11/21" --duration 25 --slides 20 --slug my-slides --thread-id run-01
   ```
   （若 PDF 先前已匯入 Wiki 但還沒擷圖，加上 `--force-extract-figures` 就會自動補擷圖！）
3. 確認大綱沒問題，輸入放行開始並行製作簡報：
   ```powershell
   python run.py resume --thread-id run-01 --approve
   ```
4. 去 `outputs\slides-html\` 打開 `.html` 預覽沒問題，輸入結案存檔至 `wiki\log.md`：
   ```powershell
   python run.py resume --thread-id run-01 --action approve
   ```
