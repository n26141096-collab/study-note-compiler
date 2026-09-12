---
name: study-note-compiler
description: 將使用者指定的 PDF、PPT、Word、Markdown、題庫與課堂筆記編譯為來源可追溯的 Markdown 與 A4 Word 複習筆記，並驗證知識單元、題庫、Coverage 與版面。適用於明確要求建立完整學習筆記；不適用於單純摘要、翻譯或一般文件排版。
metadata:
  version: "2.3.0"
---

# Study Note Compiler v2.3.0

## 0. 定位
這不是「摘要 Skill」，而是「來源受控的學習資料編譯與出版系統」。

正式流程：
`資料盤點 → 來源分級 → 題目抽取 → Knowledge Unit → 關係/因果建模 → 學習者正文 → 題庫覆蓋 → Markdown 母版 → A4 Word 真雙欄 → Readability/Render QA → Release Audit`

正式輸出至少包含：
- Markdown：內容唯一母版（Single Source of Truth）
- DOCX：只負責出版，不自行重寫內容
- `knowledge_units.yaml`：知識單元與來源定位
- `assessment.yaml`：L1–L4 題目與來源
- `coverage.yaml`：只存 evidence flags，不准手填 status
- Audit / Build Report

正式輸出分成兩層，但只維護一份內容母版：
- **來源稽核層**：YAML sidecars 保存完整八層 KU、完整 source locator、Coverage 與題庫欄位。
- **學習閱讀層**：Markdown／DOCX 用自然、連續、可口頭解釋的文字呈現；不得把 sidecar 欄位逐欄傾倒成正文。

## 閱讀路由
- 盤點或建模前，讀取 [來源治理](references/source_governance.md) 與 [專業筆記方法](references/professional_note_method.md)。
- 建立題目、Recall 或複習週期時，讀取 [學習科學規則](references/learning_science_rules.md)。
- 撰寫或改寫學習正文前，必須讀取 [學習者正文規格](references/learner_facing_writing.md)。
- 對既有編譯成果執行可閱讀化修訂或最終閱讀審查時，必須讀取 [可閱讀修訂規格](references/readable_revision.md)。
- 工程／製程／系統整合類內容適用時，額外讀取 [工程學習 Profile](references/engineering_learning_profile.md)；其他領域不得硬套工程欄位。
- 執行品質評分時，讀取 [品質 Rubric](references/professional_note_rubric.md)。
- 產生或檢查 DOCX 時，讀取 [版面規格](references/layout_reference.md)。

## 1. 來源治理
優先序：使用者指定教材 > 教師教材 > 使用者筆記 > 指定教科書/標準 > 明確要求的外部研究。

強制規則：
- 不得以模型常識默默補齊、修正或替換教材。
- 來源不足：`SOURCE_NOT_FOUND`。
- 來源衝突：`SOURCE_CONFLICT`，並列來源，不自行裁決。
- 外部補充：`EXTERNAL_RESEARCH`，不得混成原教材。
- 圖、表、公式、掃描頁無法可靠讀取：`VISUAL_CHECK_REQUIRED`。
- critical/high KU 與題目答案都必須保留結構化 source locator。

Source locator：
```yaml
file: lecture_03.pdf
locator_type: page
locator: "17"
evidence: "支持此知識點的來源摘要或短證據描述"
confidence: HIGH
```
正式教材不得用 `synthetic` locator；它只允許測試 fixture。

## 2. 執行模式
以下是此 Skill 的模式名稱，不是 Codex slash commands。明確呼叫時使用 `$study-note-compiler`。

### `$study-note-compiler ingest`
只盤點與來源分類，輸出 source registry、material roles、existing questions、source conflicts。

### `$study-note-compiler model`
建立 `knowledge_units.yaml`、knowledge relations 與 coverage seed，不先排版。

### `$study-note-compiler build <topic>`
生成：topic `.md/.docx`、knowledge units、assessment、coverage、audit。

### `$study-note-compiler compile`
生成 `00_總索引.md/.docx`、缺口報告、題目覆蓋、考前速背與所有主題。

### `$study-note-compiler update`
只重建受新增資料影響的 Knowledge Units、題目、Coverage 與索引。

### `$study-note-compiler readable-revise`
只針對已完成編譯的學習閱讀層進行最終可閱讀性審查與必要微調。不得重新解析來源、重建 KU 或大幅改變資料夾架構；執行前後必須核對治理 sidecar hash，並依 `KEEP > MICRO_EDIT > LOCAL_REWRITE > RESTRUCTURE` 決定修改幅度。輸出 `READABLE_REVISION_REPORT.md`。

### `$study-note-compiler audit`
以唯讀方式檢查既有成果的來源治理、Coverage、內容品質、可閱讀性與出版 Gate；除非使用者另行授權，不修改筆記。

## 3. Knowledge Modeling-first
禁止「逐頁摘要」。重大知識點先建成 Knowledge Unit。

類型：concept、mechanism、workflow、cause_effect、comparison、formula、decision_rule、failure_mode、pitfall、application、interview。

critical/high KU 必須具備八層：
1. Core：一句話核心
2. What：是什麼
3. Why：為什麼重要
4. How：如何運作
5. Relationships：與其他概念如何連接
6. Application：實際怎麼用
7. Pitfalls：最容易搞錯什麼
8. Recall：考試/面試怎麼問

八層是 **knowledge model／sidecar 的完整性要求**，不是八個固定正文小標。正文必須依學科與內容選擇適合的敘事順序，把必要層融入自然段落、案例、比較或決策流程；禁止每個 KU 都機械輸出同一組 `What／Why／How／Application／Pitfall／Active Recall` 標籤。

## 4. 專業筆記骨架
- 文件標頭：編號、主題、用途、來源
- 核心主軸
- 必背關鍵字
- 先翻順序
- A｜專業重點筆記：以問題、機制、比較、流程或案例中最適合的入口自然展開，包含必要的因果、決策、應用與誤判邊界
- B｜L1–L2 基礎與解釋題：正式主題至少 10 題
- C｜L3–L4 情境與診斷題：正式主題至少 10 題
- D｜Active Recall / Feynman
- Coverage Matrix

不同學科必須調整重點：工程偏流程/機制/量測/失效；法規偏責任/例外/判斷；人文偏時間/因果/比較；商管偏框架/指標/決策；面試偏 30 秒回答與情境追問。工程主題只有在適用時才載入 `engineering_learning_profile.md`，不得將角色分工、電性或良率等工程特有欄位強加到所有學科。

正文預設採「學習閱讀版」，不是 audit dump：
- 專有名詞可保留英文，其餘優先使用自然中文。
- 先回答學習者正在判斷的問題，再引入機制與證據；不要用「本教材用來連結……的知識單元」等後設填充句。
- 因果箭頭只在真的能提升查找或比較時使用；不得用箭頭鏈取代完整解釋。
- 完整 hashed path／archive internal path 留在 YAML。正文來源註記使用人類可讀的「教材／講次／頁碼」短格式。
- L3–L4 答案優先呈現：先確認什麼 → 如何分流 → 需要什麼量測／證據 → 何時能下結論。
- Active Recall 依章節設計，不得對每個 KU 重複同一句空泛提示。

## 5. 題庫與學習科學
題目不是隨機湊數，而是由 Coverage 反向補缺。
- L1：Recall
- L2：Explain
- L3：Apply
- L4：Diagnose

每題要求：id、difficulty、knowledge_unit、expected_keywords、question、answer、source_locators。

Active Recall、Feynman、Spaced Review（預設 1/3/7/16/35 天）、Error Log 只能在 Source Gate 通過後使用。

## 6. Coverage：狀態必須由程式計算
`coverage.yaml` 不允許 `status:` 或 `computed_status:` 由人手填。

輸入只寫：
```yaml
knowledge_unit: KU_01
source: true
note: true
l1_l2: true
l3_l4: true
pitfall: true
```

`coverage_audit.py` 計算：
- GAP：source 或 note 缺失
- PARTIAL：題目或 pitfall 等必要層未滿
- PASS：所有適用層皆滿

因此不存在「全部 false 但手填 PASS」的漏洞。

## 7. Markdown 是唯一內容母版
DOCX renderer 不得自行摘要、改寫答案、補來源、刪內容。版面由 Markdown layout marker 控制。

每個 critical/high KU 必須在 A 區實質內容前放置唯一 marker：
```markdown
<!-- ku: KU_01 -->
```
marker 後、下一個 marker 或 B 區之前至少要有 120 個實質字元。Coverage Matrix 中只出現 KU ID 不算筆記內容覆蓋。

KU marker 可以維持稽核映射，但不代表正文必須顯示 KU schema 欄位。每個 KU block 應像一段可獨立學習的講解，而不是 YAML 的視覺化版本。

## 8. Word 出版規格
### 8.1 真正 A4
自 v2.1.0 起不只在 YAML 宣告 A4，renderer 必須實際寫入 Word `page_width=210 mm`、`page_height=297 mm`，所有 continuous sections 也必須保持 A4。

### 8.2 真雙欄
```markdown
<!-- columns: 2 -->
```
內容先填左欄，再自然流到右欄；不是用 2-cell table 假裝整篇雙欄。

### 8.3 全寬
```markdown
<!-- columns: 1 -->
```
用於長表、Coverage、公式或索引。

### 8.4 Two-panel
```markdown
<!-- layout: two-panel -->
:::left
左側內容
:::right
右側內容
:::end
```
用於左右獨立資訊區，不等同流式 columns。

### 8.5 視覺規格
A4 Portrait、灰階、高資訊密度、13 mm 左右 margin、8.9 pt 左右 body、Heading keep-with-next、表頭灰底、禁止超版/截字/孤立標題。East-Asian 與 Latin font slots 分開寫入；跨系統若缺字型仍可能重新流版，因此每個正式 DOCX 都必須 Render QA。

## 9. 總索引
`00_總索引` 不是普通目錄，至少包含：
- 關鍵字 → 翻哪份 → 用途
- 題型 → 翻閱順序 → 答題主線
- 易混淆概念
- 公式/決策規則速查（適用時）
- 最後速背
- 主題 → 來源對照

目標：看到關鍵字後約 3 秒內知道要翻哪裡。

## 10. Professional Note Quality Gate
100 分：Source Fidelity 20、Knowledge Modeling 20、Relationships & Causality 15、Retrieval 15、Assessment 15、Pitfalls 10、Compression 5。

Release Ready ≥ 90，且：Source Fidelity ≥16、Knowledge Modeling ≥16、正式題數達標、Coverage 全 PASS、無 placeholder。

此 Gate 是機械式完整性/可追溯性檢查；它不取代逐來源語意審查。

### 10.1 Learner-facing Gates
正式 `build`／`compile` 除機械品質分數外，還必須通過：

- `TEMPLATE_REPETITION_GATE`：不得讓多數 KU 使用同一組可見欄位標籤，不得跨 KU 重複長篇後設句，也不得大量複製同一題幹只替換名詞。
- `LEARNER_FACING_GATE`：正文不得暴露 archive internal path 或 hashed locator；解釋、例子與來源註記須以讀者可理解的方式呈現。
- `READABILITY_GATE`：Agent／人工逐主題抽查至少 3 個 KU（不足 3 個則全查），朗讀時應像教師或資深同事在說明；若必須先理解模板欄位才能讀懂即 FAIL。

先執行 `learner_facing_audit.py` 做可機械檢查，再完成抽樣人工審查並在 Audit Report 記錄 KU ID、結果與必要修正。自動 PASS 不能取代人工 `READABILITY_GATE`。

### 10.2 Readable Revision Gate
`readable-revise` 必須依 `references/readable_revision.md` 完成 A–L 人工審查，並確認治理 sidecar 在修訂前後 hash 相同。A–L 平均分數 85–100 且無 Hard Blocker 才能宣告 `READABLE_RELEASE = PASS`；80–84 為 `PASS_WITH_MINOR_REVISION`；低於 80 或命中 Hard Blocker 為 `NEEDS_REVISION`。

## 11. Release Gates
- MATERIAL_GATE
- SOURCE_LOCATOR_GATE
- QUESTION_EXTRACTION_GATE
- KNOWLEDGE_MODEL_GATE
- NOTE_QUALITY_100_GATE
- TEMPLATE_REPETITION_GATE
- LEARNER_FACING_GATE
- READABILITY_GATE
- READABLE_RELEASE_GATE
- COVERAGE_COMPUTED_GATE
- MD_GATE
- DOCX_GATE
- A4_PAGE_SIZE_GATE
- WORD_TWO_COLUMN_GATE
- WORD_MIXED_LAYOUT_GATE
- MASTER_INDEX_GATE
- RENDER_GATE
- VISUAL_GATE
- RELEASE_MANIFEST_GATE

任一 Hard Gate FAIL，不得宣告正式完成。

## 12. 命令
先執行 runtime preflight：
```bash
python -c "import yaml, docx, lxml"
```
若缺少套件，先告知使用者並取得安裝授權，再執行 `python -m pip install -r requirements.txt`；不得默默修改環境。

```bash
python scripts/source_registry.py materials --out source_registry.csv
python scripts/source_locator_audit.py knowledge_units.yaml
python scripts/coverage_audit.py coverage.yaml \
  --knowledge knowledge_units.yaml \
  --out coverage_computed.yaml
python scripts/md_to_docx.py topic.md --out topic.docx
python scripts/validate_output.py topic.md topic.docx --profile topic
python scripts/validate_master_index.py 00_總索引.md 00_總索引.docx
python scripts/note_quality_audit.py topic.md \
  --knowledge knowledge_units.yaml \
  --assessment assessment.yaml \
  --coverage coverage.yaml
python scripts/learner_facing_audit.py topic.md --json-out learner_facing_audit.json
python scripts/render_docx.py topic.docx --out-dir qa/topic
pytest -q
```

`render_docx.py` 使用 LibreOffice，或在 Windows 退回 Microsoft Word COM，並需要 Poppler `pdftoppm`；沒有可用的 Office renderer 或 rasterizer 即 Hard FAIL，不得跳過。產生 PNG 後，必須逐頁檢查超版、截字、孤立標題、空白頁與表格可讀性，並保存 `render_report.json`。測試 fixture 若使用 `synthetic` source，可在 audit CLI 加 `--allow-synthetic`；正式教材不可。

## 13. v2.3.0 修正重點
- 新增 `readable-revise` 與唯讀 `audit` 模式，讓既有成果能在不重跑來源、不破壞治理 sidecar 的前提下完成可閱讀化微調。
- 新增 A–L 可閱讀發布審查、明確分數門檻、Hard Blocker 與修訂前後 governance hash 驗證。
- 新增可選的工程學習 Profile，補強全局位置、工程因果鏈、角色分工、問題拆解與 L3–L4 情境，但不硬編碼到非工程主題。
- 加入 MIT License、Codex 公開介面與公開發布所需的套件文件。

## 14. v2.2.0 修正重點
- 將完整八層 KU 保留在 sidecar，明確禁止把八層當成每個 KU 的固定可見模板。
- 新增來源稽核層／學習閱讀層分工；完整 locator 留在 YAML，正文只顯示人類可讀短來源。
- 新增 `TEMPLATE_REPETITION_GATE`、`LEARNER_FACING_GATE` 與人工 `READABILITY_GATE`。
- L3–L4 改以觀察、分流、量測證據與結論邊界組織，不再大量複製同一題幹。

## 15. v2.1.1 修正重點
- 將版本移至合法的 `metadata.version`，並使用 `$study-note-compiler` 呼叫模式。
- Coverage 強制與 `knowledge_units.yaml` 的 KU 集合完全一致，拒絕缺漏、重複與未知 KU。
- critical/high KU 與所有題目都必須有非空且有效的 source locator。
- Markdown 以 KU marker 綁定重大 KU 與實質內容，關鍵詞空殼不得 Release Ready。
- Release Manifest 拒絕未列入清單的額外檔案。
- 新增可執行的 DOCX → PDF → PNG render helper 與 runtime preflight。
