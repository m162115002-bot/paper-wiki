# AGENTS.md — 學術論文 LLM Wiki 知識庫規範

本文件是本論文知識庫的唯一作業規範（Single Source of Truth），適用於任何支援檔案讀寫與終端機操作的 LLM Agent（如 Claude Code、OpenAI Codex、OpenCode、Cursor 等）。若搭配 Claude Code 使用，可在專案根目錄建立 `CLAUDE.md` 並註明遵循本檔。

## 1. 核心定位與設計原則

1. **累積式知識架構**：本知識庫參考 Andrej Karpathy 的 LLM Wiki 模式，目標不是每次提問才臨時檢索 PDF，而是由 Agent 持續閱讀、拆解、跨篇連結並維護結構化的 Markdown 知識庫，最終支援**文獻回顧、跨研究比較、口報大綱與單檔可攜式 HTML 簡報**產出。

2. **全閱讀器相容（跨平台 Markdown）**：

   * 所有內部連結**一律使用標準相對路徑 Markdown 連結**（例如 `[Smith (2024)](../papers/smith-2024-cbti.md)`），**禁止使用** Obsidian 專屬的 `[[Wikilink]]` 語法，確保在 Obsidian、VS Code、Typora、GitHub、Logseq、Zettlr 皆可正常開啟與跳轉。

   * 圖片嵌入一律使用標準相對路徑 Markdown 語法（例如 `![圖 1：中介模型](../../raw/assets/smith-2024-cbti/fig1-mediation.png)`）。

   * 每頁保留標準 YAML Frontmatter 供檢索與外部工具（如 Obsidian Dataview）解析，但**正文嚴禁依賴 Dataview 程式碼區塊**；所有總表與索引均由 Agent 以純 Markdown 維護。

3. **語言與格式規範**：

   * 所有 Wiki 頁面、整理筆記、口報大綱與簡報正文統一以**繁體中文**撰寫。

   * 學術專有名詞保留英文原文，首次出現時以「繁體中文（English Term）」標示（例如「失眠認知行為治療（Cognitive Behavioral Therapy for Insomnia, CBT-I）」）。

   * 文內引用與參考文獻統一採用 **APA 7th 英文格式**。

## 2. 目錄結構與讀寫權限

```
paper-wiki/
├── AGENTS.md                   # 本規範檔（跨 Agent 通用）
├── raw/
│   ├── papers/                 # 【絕對唯讀】原始論文 PDF，維持使用者原始檔名
│   └── assets/                 # 【Agent 可寫入】依 <paper-slug>/ 子目錄存放擷取出的統計圖表
├── wiki/
│   ├── index.md                # 頂層總目錄與快速導覽
│   ├── overview.md             # 研究領域地圖、理論脈絡與核心演進
│   ├── log.md                  # 只增不減（append-only）之操作紀錄
│   ├── papers/                 # 單篇文獻頁（含 _index.md）
│   ├── concepts/               # 構念與理論頁（含 _index.md）
│   ├── methods/                # 方法、量表與統計模型頁（含 _index.md）
│   └── synthesis/              # 綜合比較、矛盾追蹤與研究缺口頁（含 _index.md）
└── outputs/
    ├── notes/                  # 主題整理筆記（嚴格僅基於 wiki/ 內容）
    ├── slides-outline/         # 口報大綱（人工審核關卡）
    └── slides-html/            # 最終單檔可攜式 HTML 簡報

```

### 權限邊界

* `raw/papers/`：**絕對唯讀（Immutable）**。嚴禁修改、重新命名、移動或刪除任何原始 PDF 檔案。

* `raw/assets/<paper-slug>/`：僅允許存放從對應 PDF 擷取出的關鍵圖表影像（建議 PNG 格式，命名具語意如 `fig1-study-flow.png`、`table2-regression.png`）。

* `wiki/` 與 `outputs/`：由 Agent 負責建立與維護；使用者負責審閱、挑選文獻與把關口報產出。

## 3. 檔名與 YAML Frontmatter 規範

### 檔案命名規則

* `raw/papers/` 維持原檔名不動。

* `wiki/papers/` 頁面檔名統一使用全小寫 ASCII slug：`firstauthor-year-short-topic.md`（以連字號 `-` 分隔，避免空白與特殊字元），並在 YAML Frontmatter 的 `source_file` 欄位記錄 `raw/papers/` 內的**精確原始檔名**。

* `wiki/concepts/`、`wiki/methods/`、`wiki/synthesis/` 檔名亦使用全小寫連字號 slug（例如 `cbt-i.md`、`isi-scale.md`、`cbti-vs-pharmacotherapy.md`）。

### 標準 YAML Frontmatter 欄位

| 頁面類型 | 必填欄位 | 
| ----- | ----- | 
| `wiki/papers/` | `title`, `authors`, `year`, `journal`, `doi`, `source_file`, `sample_size`, `population`, `design`, `measures`, `status` (`draft` / `reviewed`), `tags`, `ingested_at`, `updated_at` | 
| `wiki/concepts/` | `title`, `english_term`, `category`, `related_papers_count`, `status`, `tags`, `updated_at` | 
| `wiki/methods/` | `title`, `english_term`, `method_type` (`scale` / `statistical_model` / `paradigm` / `biomarker`), `related_papers_count`, `status`, `tags`, `updated_at` | 
| `wiki/synthesis/` | `title`, `synthesis_type` (`comparison` / `contradiction` / `research_gap` / `query_archive`), `source_papers`, `status`, `tags`, `updated_at` | 

## 4. 四類 Wiki 頁面結構模板

### 4.1 單篇文獻頁（`wiki/papers/<slug>.md`）

必含以下區塊：

1. **書目資訊（APA 7th）**：完整 APA 7th 參考文獻、DOI 與原始檔名對照。

2. **研究問題與假設**：條列核心研究目的與假設（標註頁碼）。

3. **研究對象與方法**：樣本數（$N$）、族群特徵、抽樣方式、研究設計、使用量表／儀器（連結至 `../methods/`）與統計分析方法。

4. **關鍵統計數據整理（Markdown 表格）**：將論文核心結果（樣本統計、主效果、交互作用、中介／調節係數、效果量、信賴區間與 $p$ 值）整理為結構化 Markdown 表格，忠實保留原始數值。

5. **關鍵統計圖表摘錄**：嵌入擷取至 `../../raw/assets/<paper-slug>/` 的關鍵圖表，附簡要圖說與原文頁碼。

6. **核心發現**：條列主要結論並標註頁碼（區分為「原文陳述」）。

7. **研究限制與批判評析**：區分「作者自述限制」與「批判筆記／跨篇關聯」（明確標示「跨篇推論」）。

8. **關聯概念與文獻**：以標準相對路徑連結至相關的 `concepts/`、`methods/`、`synthesis/` 與其他 `papers/`。

### 4.2 構念與理論頁（`wiki/concepts/<slug>.md`）

必含：核心定義與英文原文、理論模型與演進脈絡、目前學界共識、尚存分歧或矛盾證據、關聯量表／方法、收錄文獻清單（附 APA 引用與相對路徑連結）。

### 4.3 方法與量表頁（`wiki/methods/<slug>.md`）

必含：工具／方法簡介（英文全名與縮寫）、適用情境與計分／建模重點、已收錄文獻中的信效度與切點紀錄、常見限制與替代方案、使用本研究方法的文獻清單。

### 4.4 綜合比較與研究缺口頁（`wiki/synthesis/<slug>.md`）

必含：比較主題與收錄範圍、跨篇比較 Markdown 表格（含作者年份、樣本、設計、核心發現、效果量）、一致性與矛盾點解析、明確列出的研究缺口（Research Gaps）與後續待驗證問題。

## 5. 學術嚴謹度與反幻覺鐵律

1. **雙重溯源**：Wiki 內文與所有產出每次引用已收錄文獻時，必須同時提供 APA 7th 文內引用與標準相對路徑連結，例如 `([Smith et al., 2024](../papers/smith-2024-cbti.md))`；關鍵數據與特定論點須加註原文頁碼（如 `p. 124`）。

2. **原文陳述 vs. 跨篇推論**：清楚區隔論文原始結果與 Agent 的跨篇綜合推論，嚴禁將綜合推測寫成原論文的主張。

3. **數據忠實度**：保留原始統計指標（如 $N$, $M$, $SD$, $t$, $F$, $\beta$, $r$, $d$, $\eta_p^2$, OR, 95% CI, $p$），不得自行估算或竄改顯著性判讀；若原文未報告特定指標，明寫「原文未報告」。

4. **嚴格 Wiki 邊界與 `[Wiki 缺口]` 標記**：

   * 產出 `outputs/notes/`、`outputs/slides-outline/`、`outputs/slides-html/` 或進行知識庫問答時，**正文嚴格只能使用 `wiki/` 內已收錄的文獻內容**。

   * 凡論證過程發現知識庫尚未涵蓋的證據、理論或數據，必須在該處明確標註 `[Wiki 缺口: 目前知識庫尚未收錄 XX]`。

   * 若使用者允許或需要外部補充建議，未收錄之外部文獻**只能**列於文件最末端的「建議後續收錄文獻」區塊，並附推薦理由，嚴禁混入正文。

## 6. 數百篇規模之三段式檢索策略

本知識庫預期累積至數百篇文獻。為避免上下文過載與遺漏，執行 Query、Ingest 關聯檢查或產出筆記時，**禁止一次讀取全部 `wiki/` 檔案**，一律依序採用三段式檢索：

1. **第一段（本地搜尋定位）**：

   * 若執行環境已安裝 `qmd`，優先呼叫 `qmd` 進行語意與關鍵字混合檢索。

   * 若無 `qmd`，使用終端機工具（如 `rg` / `grep`）針對 `wiki/` 的 YAML Frontmatter（`tags`、`year`、`design`、`measures`、`population`）與關鍵詞篩選候選檔案。

2. **第二段（分層索引過濾）**：

   * 讀取 `wiki/index.md` 與相關分類的 `_index.md`（`wiki/papers/_index.md`、`wiki/concepts/_index.md`、`wiki/methods/_index.md`、`wiki/synthesis/_index.md`），縮小至最相關的 5–15 篇頁面。

3. **第三段（精準深讀）**：

   * 僅開啟鎖定的候選頁面與對應的 `synthesis/` 頁面進行綜合分析與寫作。

## 7. 四大核心作業流程

### 7.1 Ingest（文獻匯入）— 支援雙模式

#### 模式 A：單篇精讀模式（預設）

1. 讀取 `raw/papers/` 中指定的原始 PDF。

2. 擷取關鍵統計圖表存至 `raw/assets/<paper-slug>/`，並將重要統計數據整理成 Markdown 表格。

3. **互動確認**：先在對話中向使用者摘要研究重點、核心數據、與既有 Wiki 的潛在連結或矛盾，詢問是否有特別想強調的批判觀點或標籤。

4. 經確認後，建立 `wiki/papers/<paper-slug>.md`（`status: reviewed`），並同步更新相關的 `concepts/`、`methods/`、`synthesis/` 頁面。

5. 更新對應的分類 `_index.md`、`wiki/index.md`、`wiki/overview.md`（若有結構性進展），並於 `wiki/log.md` 追加紀錄。

#### 模式 B：批次匯入模式（適用一次匯入多篇 PDF）

1. 掃描使用者指定的多篇 PDF（或 `raw/papers/` 中尚未收錄的檔案）。

2. 逐篇完成基礎擷取：擷取關鍵統計圖表至 `raw/assets/<paper-slug>/`、建立 `wiki/papers/<paper-slug>.md`（標記 `status: draft`）並整理核心統計 Markdown 表格。

3. 批次更新 `wiki/papers/_index.md`、`wiki/index.md` 與 `wiki/log.md`。

4. 批次結束後，在對話中提供一份**跨篇彙整清單**（列出共通主題、潛在矛盾結果、建議新建或更新的 `concepts/`、`methods/`、`synthesis/` 頁面），待使用者確認後再進行跨頁深化，並將對應頁面更新為 `status: reviewed`。

### 7.2 Query（知識庫問答與回存）

1. 依「三段式檢索策略」查詢 `wiki/`，嚴格遵守 APA 7th + 相對路徑連結與 `[Wiki 缺口: ...]` 規則作答。

2. 若該次查詢產出具累積價值的跨篇比較表、理論對照或研究缺口分析，主動詢問使用者是否回存至 `wiki/synthesis/<slug>.md`；若確認回存，同步更新 `wiki/synthesis/_index.md`、`wiki/index.md` 與 `wiki/log.md`。

### 7.3 Lint（結構與論文專屬健康檢查）

定期或依使用者指示執行健康檢查，產出檢查報告並在確認後修復：

| 檢查類別 | 具體檢查項目 | 
| ----- | ----- | 
| **結構完整性** | 孤兒頁（無入站連結）、斷鏈（含相對路徑與 `raw/assets/` 圖片路徑）、`source_file` 與 `raw/papers/` 原檔對應是否正確、各分類 `_index.md` 與實際檔案是否同步。 | 
| **引用一致性** | APA 7th 文內引用格式是否一致、是否遺漏相對路徑連結或關鍵數據頁碼。 | 
| **薄弱證據警示** | 標出 `concepts/` 與 `synthesis/` 中「僅靠單一小樣本研究（或單一研究團隊）」支撐的重要論點。 | 
| **年份演變與矛盾** | 檢查較早期文獻結論是否被近年研究修正、推翻，或在不同族群／量表下出現矛盾，並提醒更新 `synthesis/`。 | 
| **關鍵文獻缺口** | 統計被多篇已收錄論文高頻引用、但 `raw/papers/` 尚未收錄的奠基文獻或關鍵量表原始論文，列出補讀清單。 | 
| **草稿狀態追蹤** | 列出仍停留在 `status: draft`、尚未完成跨頁整合的文獻頁。 | 

### 7.4 口報大綱與單檔可攜式 HTML 簡報管線（Human-in-the-Loop）

從知識庫產出學術口頭報告時，嚴格遵循三階段流程，**每階段完成後必須暫停並等待使用者確認**，才可進入下一階段：

1. **階段一：主題整理筆記（`outputs/notes/<topic-slug>.md`）**

   * 依三段式檢索策略從 `wiki/` 彙整論點、Markdown 統計表格、擷取圖表與 APA 7th 引用。

   * 嚴格遵守 Wiki 邊界，缺漏處標註 `[Wiki 缺口: ...]`；未收錄的外部文獻僅列於文末建議清單。

2. **階段二：口報大綱（`outputs/slides-outline/<topic-slug>-outline.md`）**

   * 依確認後的筆記規劃投影片架構，每頁須明確列出：

     * **結論式標題（Action Title）**

     * **核心呈現要點**（精簡條列或對照表格）

     * **預計嵌入圖表**（對應 `raw/assets/` 圖片或需繪製的視覺圖）

     * 口報講者備忘錄（Speaker Notes）與預估時間分配

     * **頁尾 APA 7th 出處**

3. **階段三：單檔可攜式 HTML 簡報（`outputs/slides-html/<topic-slug>-slides.html`）**

   * 產出**單一自包含（Self-contained）HTML 檔案**：所有 CSS 與 JavaScript 內嵌於單一檔案；若引用 `raw/assets/` 中的統計圖表，將圖片轉為 Base64 Data URI 內嵌，確保離線或複製到其他電腦開啟皆不破圖。

   * **必備功能**：

     * 支援鍵盤左右鍵／空白鍵切換投影片與滑鼠點擊導覽。

     * 頂部或底部進度條與目前頁碼（如 `3 / 15`）。

     * 可切換顯示／隱藏的講者備忘錄（Speaker Notes）面板（例如按 `N` 鍵開關）。

     * 完整 `@media print` 樣式，支援瀏覽器直接列印／匯出乾淨分頁之 PDF。

   * **學術視覺規範**：每頁清楚保留精簡 APA 7th 引用來源，末頁自動彙整完整 APA 7th 參考文獻清單，並於 `wiki/log.md` 記錄本次產出。

## 8. `wiki/log.md` 紀錄格式

`wiki/log.md` 為只增不減（append-only）紀錄檔。每次完成 Ingest、批次匯入、Query 回存、Lint 或簡報產出時，皆須於檔尾追加一筆標準格式紀錄，方便以 Unix 工具（如 `grep "^## \[" wiki/log.md | tail -10`）快速追蹤：

```
## [YYYY-MM-DD] <ingest|batch-ingest|query|lint|slides> | <簡短標題>
- 影響檔案：<列出新增或更新之主要相對路徑>
- 摘要：<1–3 句說明完成內容、發現的關鍵矛盾或待處理缺口>

```