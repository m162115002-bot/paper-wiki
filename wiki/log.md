# 操作時間軸紀錄（Log）

本檔為只增不減（append-only）之操作紀錄，可使用 `grep "^## \[" wiki/log.md | tail -10` 快速查詢近期進度。

## [2026-11-21] init | 初始化學術論文 LLM Wiki 知識庫
- 影響檔案：`AGENTS.md`、`CLAUDE.md`、`wiki/index.md`、`wiki/overview.md`、`wiki/log.md`、各分類 `_index.md`
- 摘要：完成獨立論文知識庫初始目錄結構與核心規範建置，準備匯入首批原始論文 PDF。

## [2026-11-21] ingest | Sarafino & Smith (2017) Ch. 11 The Nature and Symptoms of Pain
- 影響檔案：`wiki/papers/sarafino-ch11-nature-symptoms-of-pain.md`、`wiki/concepts/`（5 頁）、`wiki/methods/`（4 頁）、`raw/assets/sarafino-ch11-nature-symptoms-of-pain/`（7 張圖表）、`wiki/index.md`、`wiki/overview.md` 及各分類 `_index.md`
- 摘要：完成首篇文獻單篇精讀匯入，建立疼痛生物心理社會基礎架構、9 項關鍵實證數據表格與 7 張擷取圖表；後續可持續補齊原始期刊論文並開啟 `wiki/synthesis/` 跨篇比較。

## [2026-11-21] slides | Chapter 11: The Nature and Symptoms of Pain（日式可愛粉彩版 + LangGraph 管線）
- 影響檔案：`outputs/slides-outline/ch11-nature-symptoms-of-pain-outline.md`、`outputs/slides-html/ch11-nature-symptoms-of-pain-slides.html`、`scripts/slide_graph/`
- 摘要：建置 LangGraph + Gemini API 自動化投影片管線（Map-Reduce 分單元並行＋局部重試＋條件式 HITL），並實際產出第 11 章 22 頁日式可愛粉彩單檔 HTML 簡報（內嵌 7 張 Base64 課本原圖與口語講稿）。

## [2026-11-21] ingest | Edward P. Sarafino et al. (2017) Chapter 12: Managing and Controlling Clinical Pain
- 影響檔案：`wiki/papers/sarafino-ch12-managing-controlling-clinical-pain.md`, `wiki/concepts/operant-pain-management.md`, `wiki/concepts/cognitive-coping-and-redefinition.md`, `wiki/methods/transcutaneous-electrical-nerve-stimulation.md`
- 摘要：本文為《健康心理學》第十二章，系統性探討臨床疼痛（包含急性與慢性痛）的多元管理與控制方法。內容涵蓋手術與化學藥物治療（如非類固醇消炎止痛藥、鴉片類藥物與病患自控式止痛）、行為與認知方法（如操作制約、放鬆訓練、生理回饋、分心、引導式想像與疼痛重構）、催眠與人際治療、刺激與物理治療（如 TENS、針灸、物理運動），以及整合上述多專科機制的疼痛診所。文獻強調單一醫療介入往往不足，必須透過生物心理社會模式（Biopsychosocial Model）與跨領域團隊合作，才能達到最佳止痛、降低用藥與恢復生活功能的長期療效。

## [2026-11-21] slides | Chapter 12: 臨床疼痛的管理與控制
- 影響檔案：`outputs\slides-html\ch12-pain-management-slides.html`
- 摘要：透過 LangGraph + Gemini API 自動化管線產出 20 頁日式可愛粉彩單檔 HTML 簡報。

## [2026-11-21] ingest | Edward P. Sarafino et al. (2017) Chapter 12: Managing and Controlling Clinical Pain
- 影響檔案：`wiki/papers/sarafino-ch12-managing-controlling-clinical-pain.md`；擷取圖表 3 張
- 摘要：本專章系統性探討臨床疼痛（clinical pain）之生物心理社會整合治療取向。首先區分急性與慢性臨床疼痛在生理機制與心理衝擊之差異，評估外科手術與四類鎮痛藥物之效能與侷限。其次詳述行為與認知介入策略，包含操作制約技術、減恐暴露、漸進式肌肉放鬆、生理回饋、主動應對策略（分心、意象、疼痛重構）及接納與承諾治療（ACT）。此外，專章評估了催眠、人際心理治療、經皮神經電刺激（TENS）、針灸及物理治療等刺激與物理介入。最後總結多科整合疼痛診所（multidisciplinary pain clinics）之跨專業團隊模式，證實結合醫學、認知行為與物理治療之整合方案能顯著降低失能、用藥與自評疼痛，並促進長期重返職場。

## [2026-11-21] slides | Chapter 12: 臨床疼痛的管理與控制
- 影響檔案：`outputs\slides-html\ch12-with-figs-slides.html`
- 摘要：透過 LangGraph v3 一條龍管線（自動匯入與圖表擷取＋分單元並行）產出 20 頁日式可愛粉彩單檔 HTML 簡報。

## [2026-11-21] ingest | Edward P. Sarafino et al. (2017) Using Health Services (Chapter 9)
- 影響檔案：`wiki/papers/sarafino-ch09-using-health-services.md`；擷取圖表 0 張
- 摘要：本章探討個體如何感知與詮釋身體症狀、使用與誤用醫療服務的心理社會機制，以及醫病關係對醫療順從性（Compliance / Adherence）的關鍵影響。研究指出，症狀感知不僅受客觀生理訊號影響，更顯著受到環境競爭刺激、認知期望（如安慰劑與反安慰劑效應）、個案研究與社會暗示（如醫學生病、集體心因性疾病）之調節。個體建構的「常識疾病模型」（Commonsense Models of Illness）包含疾病身分、病因、時間線與後果四要素，直接決定其求醫決策與非正式轉介網絡（Lay Referral Network）的使用。求醫延誤可分為評估延誤、疾病延誤與利用延誤三個階段，各有其特定的影響因子。此外，醫師採用患者中心風格（Patient-Centered Style）而非醫師中心風格（Doctor-Centered Style），能顯著改善醫病溝通並提升個案的順從性；透過行為客製化、自我監測與行為契約等策略可大幅降低醫療不順從（Rational & Unintentional Nonadherence）所帶來的健康風險與經濟負擔。

## [2026-11-21] ingest | Edward P. Sarafino et al. (2017) 第十章 醫院：環境、醫療處置與對病患的心理影響
- 影響檔案：`wiki/papers/sarafino-2017-ch10-hospital-setting-effects.md`, `wiki/concepts/depersonalization-in-healthcare.md`, `wiki/concepts/hospital-burnout.md`, `wiki/concepts/sick-role-reactance.md`, `wiki/concepts/psychological-preparation-for-medical-procedures.md`, `wiki/concepts/child-hospitalization-distress.md`, `wiki/concepts/terminal-illness-and-palliative-care.md`, `wiki/methods/millon-behavioral-medicine-diagnostic.md`, `wiki/methods/psychosocial-adjustment-to-illness-scale.md`；擷取圖表 7 張
- 摘要：本章深入剖析現代醫院環境對病患與醫事人員之心理社會影響。住院歷程伴隨高度依賴性、隱私喪失與對醫療程序的預期焦慮，易引發病患的去控制感與情緒適應障礙。研究指出，透過提供行為控制（Behavioral Control）、認知控制（Cognitive Control）與資訊控制（Informational Control）之心理準備，能有效降低手術與侵入性檢查前的焦慮，並顯後改善術後併發症與血壓異常。然而，心理準備之成效受到患者應對風格（注意力型 Monitors vs. 迴避型 Blunters）之調節，訊息過載反倒可能提升迴避型患者的壓力。針對兒童患者，同房陪病與發育匹配的心理準備可緩解分離焦慮（Separation Distress）；對於末期臨終患者，安寧療護（Hospice Care）則提供兼顧身體疼痛控制與心理靈性支持的整體照護方案。

## [2026-11-21] ingest | Edward P. Sarafino et al. (2017) Chapter 13: Serious and Disabling Chronic Illnesses: Causes, Management, and Coping
- 影響檔案：`wiki/papers/sarafino-2017-ch13-disabling-chronic-illnesses.md`, `wiki/concepts/crisis-theory-of-chronic-illness.md`, `wiki/concepts/self-management-in-chronic-illness.md`, `wiki/concepts/dementia-caregiver-burden.md`, `wiki/methods/arthritis-self-management-program.md`, `wiki/methods/integrated-care-for-chronic-illness.md`；擷取圖表 8 張
- 摘要：本章探討個體與家庭面對嚴重且致殘性慢性疾病（如哮喘、癲癇、脊髓損傷、糖尿病、關節炎及阿茲海默症）時的心理適應歷程與介入策略。個體接獲診斷初期常經歷震驚與否認，隨後依據 Moos 的危機理論（Crisis Theory），透過疾病相關因素、個人背景及環境因素的相互作用，進行認知評估並展開適應任務與應對技巧。文中詳細分析各主要慢性病的神經生理學機制、治療方案及其所引發的心理社會挑戰（如污名化、憂鬱、依從性低下與照顧者耗竭）。最後，專章回顧了結合教育、社會支持、行為介入、放鬆與生物回饋、認知重構、家庭治療及協同照護（Integrated Care）等綜合心理社會處置在提升慢性病患者生活品質上的實質效益。

## [2026-11-21] slides | 健康心理學論文知識庫綜合導讀
- 影響檔案：`outputs\slides-html\five-papers-deck-slides.html`
- 摘要：透過 LangGraph v3 一條龍管線（自動匯入與圖表擷取＋分單元並行）產出 20 頁日式可愛粉彩單檔 HTML 簡報。

## [2026-11-21] slides | Chapter 11: 疼痛的本質與症狀
- 影響檔案：`outputs\slides-html\ch11-demo-run-slides.html`
- 摘要：透過 LangGraph v3 一條龍管線（自動匯入與圖表擷取＋分單元並行）產出 20 頁日式可愛粉彩單檔 HTML 簡報。

## [2026-11-22] slides | 嚴重與失能的長期疾病
- 影響檔案：`outputs\slides-html\new-topic-slides.html`
- 摘要：透過 LangGraph v3 一條龍管線（自動匯入與圖表擷取＋分單元並行）產出 20 頁日式可愛粉彩單檔 HTML 簡報。

## [2026-11-22] slides | 醫院設定、過程與對病患的效果
- 影響檔案：`outputs\slides-html\new-topic-slides.html`
- 摘要：透過 LangGraph v3 一條龍管線（自動匯入與圖表擷取＋分單元並行）產出 31 頁日式可愛粉彩單檔 HTML 簡報。
