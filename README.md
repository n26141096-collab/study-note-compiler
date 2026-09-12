# Study Note Compiler v2.3.0

[![Latest release](https://img.shields.io/github/v/release/n26141096-collab/study-note-compiler?label=release)](https://github.com/n26141096-collab/study-note-compiler/releases/latest)
[![Discussions](https://img.shields.io/github/discussions/n26141096-collab/study-note-compiler?label=心得與問答)](https://github.com/n26141096-collab/study-note-compiler/discussions)
[![Issues](https://img.shields.io/github/issues/n26141096-collab/study-note-compiler?label=問題回報)](https://github.com/n26141096-collab/study-note-compiler/issues)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

把 PDF、PPT、Word、Markdown、題庫與課堂筆記，編譯成**來源可追溯的 Markdown 母版**與**適合列印閱讀的 A4 Word 複習筆記**。

> 它不是單純摘要器。流程會先建立知識單元，再治理來源定位、題庫 Coverage、筆記結構、可閱讀性與 Word Render QA。

## 從這裡開始

| 你的目的 | 前往 |
|---|---|
| 下載可安裝版本 | [Latest release](https://github.com/n26141096-collab/study-note-compiler/releases/latest) |
| 先了解流程與審查標準 | [公開說明 PDF](Study_Note_Compiler_Skill_邏輯說明.pdf) |
| 分享使用心得或成果 | [Discussions](https://github.com/n26141096-collab/study-note-compiler/discussions) |
| 詢問使用方法 | [Q&A](https://github.com/n26141096-collab/study-note-compiler/discussions/categories/q-a) |
| 回報錯誤 | [Issues](https://github.com/n26141096-collab/study-note-compiler/issues)（登入後選擇 New issue） |
| 提出功能建議 | [Issues](https://github.com/n26141096-collab/study-note-compiler/issues)（登入後選擇 New issue） |

## 你會得到什麼

- 一份可長期維護、可追溯來源的 Markdown 母版。
- 一份 A4 Word 複習筆記，支援真雙欄與混合版面。
- Knowledge Unit、題庫、Coverage 與來源定位的結構化治理。
- 針對既有筆記的 `readable-revise` 可閱讀修訂與 A–L 審查。
- 工程／製程／系統整合主題可選用工程學習 Profile。

## 3 步驟安裝

### 1. 下載

從 [Latest release](https://github.com/n26141096-collab/study-note-compiler/releases/latest) 下載 `study-note-compiler-v2.3.0.zip` 並解壓縮。

### 2. 放入 Codex Skill 目錄

Repository 專用：

```text
.agents/skills/study-note-compiler/SKILL.md
```

或放入個人 skills 目錄，供多個專案使用：

```text
~/.codex/skills/study-note-compiler/SKILL.md
```

### 3. 開始使用

開啟新的 Codex task，附上或指定教材位置，使用以下提示：

```text
使用 $study-note-compiler 的 compile 模式，將我指定的教材整理成來源可追溯、適合真正學習的 Markdown 與 A4 Word 複習筆記；完成所有 Coverage、來源定位、內容品質及 Render QA。
```

`ingest`、`model`、`build`、`compile`、`update`、`readable-revise`、`audit` 是 Skill 模式，不是 slash commands。

## 常用模式

| 模式 | 適用情境 |
|---|---|
| `compile` | 從正式來源建立完整、可追溯的學習筆記 |
| `update` | 只更新受新增資料影響的知識單元、題目、Coverage 與索引 |
| `readable-revise` | 不重跑來源、不重建知識單元，只改善既有筆記的學習閱讀層 |
| `audit` | 唯讀檢查成果，不修改檔案 |

工程／製程／系統整合主題可載入 release 套件內的 `references/engineering_learning_profile.md`，建立「參數 → 機制 → 結果 → 量測 → 失效 → 性能／電性 → 良率／可靠度」與角色分工；其他學科不會被強制套用工程格式。

## 使用後請留下心得

你的回饋會直接影響下一版的安裝流程、審查標準與輸出品質。請到 [Discussions](https://github.com/n26141096-collab/study-note-compiler/discussions) 分享：

- 使用情境與教材類型。
- 是否成功產生 Markdown 與 Word。
- 最有幫助的功能。
- 卡住的步驟與改善建議。

請勿上傳含有個資、未授權教材或受著作權保護的完整內容；可使用匿名化截圖或只描述流程。

## 問題與貢獻入口

- 使用心得、成果展示、一般問答：[Discussions](https://github.com/n26141096-collab/study-note-compiler/discussions)
- 可重現的錯誤與功能需求：[Issues](https://github.com/n26141096-collab/study-note-compiler/issues)（登入後選擇 New issue）
- 提交修改：[Pull requests](https://github.com/n26141096-collab/study-note-compiler/pulls)
- 版本內容與安裝包：[Releases](https://github.com/n26141096-collab/study-note-compiler/releases)

## 重要邊界

這是一套 **Agent/LLM workflow + deterministic publishing/audit scripts**。Python scripts 不會自行理解原始教材、也不會偷偷摘要 PDF；來源閱讀、知識建模與語意忠實度必須由可讀取來源的 Agent 或人工執行。Scripts 負責結構、可追溯性、題數、Coverage、DOCX 與 release integrity。

## Runtime

```bash
python -c "import yaml, docx, lxml"
python -m pip install -r requirements.txt
```

缺少依賴時，Agent 必須先取得使用者同意才可安裝。

## Smoke test

```bash
python scripts/coverage_audit.py examples/sample_coverage.yaml --knowledge examples/sample_knowledge_units.yaml --out coverage_computed.yaml
python scripts/source_locator_audit.py examples/sample_knowledge_units.yaml --allow-synthetic
python scripts/source_locator_audit.py examples/sample_assessment.yaml --allow-synthetic
python scripts/md_to_docx.py examples/sample_topic.md --out examples/sample_topic.docx --course "Study Note QA"
python scripts/validate_output.py examples/sample_topic.md examples/sample_topic.docx --profile topic
python scripts/note_quality_audit.py examples/sample_topic.md \
  --knowledge examples/sample_knowledge_units.yaml \
  --assessment examples/sample_assessment.yaml \
  --coverage examples/sample_coverage.yaml \
  --allow-synthetic
python scripts/learner_facing_audit.py examples/sample_topic.md
pytest -q
```

## Word shipping gate

每個最終 DOCX 都必須執行：

```text
python scripts/render_docx.py topic.docx --out-dir qa/topic
→ 每頁 PNG
→ 100% 視覺檢查
→ 修正
→ 重新 render
```

此 helper 使用 LibreOffice，或在 Windows 退回 Microsoft Word COM，並需要 Poppler `pdftoppm`；沒有 Render QA 就不能宣告完成。

## 公開使用與授權

程式、模板與 Skill 規則依 [MIT License](LICENSE) 公開，著作權人為 JYUN。使用者可依授權條款使用、修改與散布本 Skill。

本授權只涵蓋這個 Skill 套件本身，不會替輸入教材或生成筆記取得再散布權。公開筆記前仍須確認原始 PDF、投影片、圖片、題庫及引用內容的著作權與使用範圍；Skill 不會自動發布任何來源材料。
