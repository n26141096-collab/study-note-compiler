# Study Note Compiler v2.3.0｜公開發布嚴格審查報告

日期：2026-09-01

著作權人：JYUN  
授權：MIT License

## 最終裁決

```text
RELEASE=study-note-compiler-v2.3.0
SKILL_QUICK_VALIDATE=PASS
PYTHON_AST_PARSE=PASS
PYTEST=PASS_17_OF_17
SOURCE_LOCATOR_GATE=PASS_4_KU_20_QUESTIONS
COVERAGE_COMPUTED_GATE=PASS_4_OF_4
PROFESSIONAL_NOTE_QUALITY_SAMPLE=PASS_100_OF_100
TEMPLATE_REPETITION_SAMPLE=PASS
LEARNER_FACING_SAMPLE=PASS
READABILITY_SAMPLE=PASS_KU_PROBLEM_KU_CAUSALITY_KU_CLOSURE
READABLE_RELEASE_SPEC=PASS_A_TO_L_WITH_HARD_BLOCKERS
READABLE_RELEASE_SAMPLE=PASS_94_OF_100
GOVERNANCE_NON_REGRESSION=PASS_4_OF_4_SIDECARS_UNCHANGED
ENGINEERING_PROFILE=PASS_OPTIONAL_AND_DOMAIN_SCOPED
LEGACY_FAB_ETCH_FORWARD_TEST=REJECTED_4_EXPECTED_ISSUES
ADVERSARIAL_KEYWORD_SHELL=REJECTED
ADVERSARIAL_PARTIAL_COVERAGE=REJECTED
ADVERSARIAL_MISSING_MAJOR_LOCATOR=REJECTED
ADVERSARIAL_UNLISTED_RELEASE_FILE=REJECTED
A4_PAGE_SIZE=PASS_3_OF_3_SECTIONS
WORD_REAL_TWO_COLUMN=PASS
WORD_MIXED_LAYOUT=PASS
WORD_TWO_PANEL=PASS_EXPLICIT_DXA_GEOMETRY
MASTER_INDEX_VALIDATOR=PASS
RENDER_GATE=PASS_TOPIC_2_PAGES_MASTER_1_PAGE
VISUAL_GATE=PASS_3_OF_3_PAGES_INSPECTED
PUBLIC_INTERFACE=PASS
MIT_LICENSE=PASS_COPYRIGHT_JYUN
RELEASE_MANIFEST_GATE=PASS
HARD_BLOCKERS=0
RELEASE_STATUS=READY
```

## 1. v2.3.0 公開版同步

- 新增 `readable-revise`：只修既有成果的學習閱讀層，不重新解析來源、不重建 KU、不大幅改變資料夾架構。
- 新增唯讀 `audit` 模式，避免「只想審查」被誤執行為重編譯。
- 修訂前後以 governance sidecar hash 驗證非回歸；採 `KEEP > MICRO_EDIT > LOCAL_REWRITE > RESTRUCTURE`。
- 新增 A–L 可閱讀發布審查、85／80 分門檻與 Hard Blocker。
- 新增章首「本章大圖」與可選工程學習 Profile；工程因果鏈、角色分工、問題拆解與 L3–L4 情境只在領域適用時啟用。
- 新增 MIT License、JYUN 著作權聲明與 `agents/openai.yaml` 公開介面。

## 2. A–L 可閱讀發布抽樣

| 維度 | 分數 | 判定摘要 |
|---|---:|---|
| A｜模板痕跡 | 90 | 主要內容可自然朗讀，fixture 標示只服務測試辨識 |
| B｜章首大圖 | 94 | 先交代角色、上下游、資料鏈與失敗風險 |
| C｜學習順序 | 92 | 由問題定義進入流程、commonality、因果與 closure |
| D｜因果推理 | 95 | 清楚區分 correlation、causality 與 root cause |
| E｜實務判斷 | 94 | 包含確認、圍堵、分流、驗證與結論邊界 |
| F｜角色分工 | 92 | 單站 owner 與 integration owner 關注點可區分 |
| G｜情境題品質 | 91 | L3–L4 以資料不足、假設排除與下一步量測為主 |
| H｜來源追溯 | 100 | synthetic fixture 明確標示；正式來源規則未放寬 |
| I｜快速複習 | 93 | 核心主軸、翻閱順序、快速複習與 Recall 可定位 |
| J｜面試實用 | 93 | 能形成短答、追問與診斷主線 |
| K｜後續擴充 | 92 | Profile 與 case 結構可擴充且不綁死單一領域 |
| L｜治理保護 | 100 | 四份既有 sidecar 與 v2.2.0 manifest hash 相同 |

平均 93.8，四捨五入為 94；無 Hard Blocker，因此抽樣裁決為 `READABLE_RELEASE = PASS`。此分數驗證公開 fixture 與規格，不代表未經審查的新教材會自動得到同一分數。

## 3. v2.2.0 閱讀體驗修正（保留為回歸基線）

- 八層 KU 保持 sidecar 完整，但不再強迫 Markdown 逐欄顯示 What／Why／How／Application／Pitfall／Recall。
- 新增 `references/learner_facing_writing.md`，定義來源稽核層與學習閱讀層。
- 完整 hashed locator 與 archive internal path 留在 YAML；正文只使用教材／講次／頁碼短來源。
- L3–L4 改以「先確認 → 分流 → 量測／證據 → 結論邊界」組織。
- 人工 Readability Gate 抽查 `KU_PROBLEM`、`KU_CAUSALITY`、`KU_CLOSURE`，三者均可脫離 sidecar 自然朗讀與重述。

## 4. Learner-facing 對抗測試

新版 `learner_facing_audit.py` 對舊版 FAB Etch 筆記正確拒絕：

- `TEMPLATE_VISIBLE_LABEL_GRID`
- `TEMPLATE_REPEATED_LONG_SENTENCE`
- `TEMPLATE_REPEATED_QUESTION_STEM`
- `LEARNER_FACING_RAW_ARCHIVE_LOCATOR`

v2.2.0 示範筆記通過 `TEMPLATE_REPETITION_GATE` 與 `LEARNER_FACING_GATE`；腳本仍只列出人工抽樣 KU，不得自行宣告 `READABILITY_GATE`。

## 5. Skill 格式與呼叫方式

- `SKILL.md` 已通過官方 `quick_validate.py`。
- 版本從非法的頂層 `version` 移至 `metadata.version`。
- 模式改用 `$study-note-compiler ingest|model|build|compile|update|readable-revise|audit`，不再宣稱註冊 `/study` slash command。
- `SKILL.md` 已加入 references 路由與 runtime preflight；缺少 Python 套件時必須先取得安裝授權。

## 6. Source Locator Gate

`source_locator_audit.py` 現在逐一檢查物件，而不是只遍歷已存在的 locator：

- 每個 critical/high KU 必須有非空 `source_locators`。
- 每道題目都必須有非空 `source_locators`。
- 重複 ID、非 list locator、欄位缺失、synthetic 正式來源都會失敗。

負向案例「一個重大 KU 有 locator、另一個完全缺 locator」已確認被拒絕。

## 7. Coverage Gate

`coverage_audit.py --knowledge knowledge_units.yaml` 現在強制：

- Coverage KU 集合與 Knowledge Unit 集合完全一致。
- 不得缺少、重複或加入未知 KU。
- `status` / `computed_status` 仍禁止手填。
- `l3_l4_required` 與 `pitfall_required` 使用嚴格布林解析，字串 `false` 不再被 Python truthiness 誤判。

負向案例「4 個 KU 只列 1 個 Coverage row」已確認被拒絕。

## 8. Markdown 與 Quality Gate

每個 critical/high KU 必須在 A 區使用唯一 marker：

```markdown
<!-- ku: KU_ID -->
```

marker 後到下一 marker 或 B 區之前必須至少有 120 個實質字元。Quality score 的 Knowledge Modeling 現在同時包含 sidecar 八層完整度與 Markdown KU block 覆蓋。

負向案例只保留「核心主軸、關鍵字、先翻順序、最後速背、Active Recall、Feynman、Coverage Matrix」等關鍵詞，沒有任何黑名單句子，仍會因 `NOTE_KU_COVERAGE_INCOMPLETE` 被拒絕。

renderer 已修正為忽略一般 HTML comments，KU marker 不會出現在 Word 正文。

## 9. DOCX 結構與實際 Render QA

重新由 `examples/sample_topic.md` 產生 DOCX 後，結構檢查結果：

- 3 sections 全部為實體 A4。
- 1 個真雙欄 section、2 個單欄 section。
- Topic 與 Master Index validator 均通過。

`scripts/render_docx.py` 支援：

- LibreOffice headless；或
- Windows Microsoft Word COM fallback；
- Poppler `pdftoppm` 逐頁轉 PNG。

本次以 Microsoft Word COM + Poppler 實際 render 主題 2 頁與總索引 1 頁並逐頁檢查。初次發現 two-panel 表格缺少明確寬度，造成窄字與空白頁；已改為固定 DXA table／grid／cell geometry並加入回歸測試。最終 3 頁均無 KU marker 外洩、截字、重疊、表格超版、缺字或多餘空白頁。

## 10. Release Manifest

Manifest auditor 現在比較實際檔案集合與 `manifest.txt`，只忽略明確的 `.pytest_cache`、`__pycache__` 與 `qa` 目錄。任意未列入的額外檔案會觸發 `UNLISTED_FILE`，缺檔也不會再因後續 hash 讀取而崩潰。

## 11. 誠實邊界

- 100 分 Quality Gate 是機械式結構、可追溯性、Coverage 與明顯缺陷檢查，不自動證明來源語意為真。
- 正式教材仍需來源感知的 Agent 或人工核對 evidence、公式、圖表與 paraphrase。
- 每個新產生的正式 DOCX 仍必須重新 render 與逐頁視覺檢查；本報告只證明 v2.3.0 公開範例與工具鏈通過。
- MIT License 只授權本 Skill 套件；輸入教材、圖片、題庫與生成筆記仍須另行確認公開散布權。
- 本次未重新編譯、解析或修改既有 `FAB_PE_PI_STUDY_NOTES`。
