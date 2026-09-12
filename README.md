# study-note-compiler v2.3.0

來源受控且以學習者為中心的專業複習筆記 Skill：Knowledge Modeling-first、結構化來源定位、自然學習正文、Coverage-computed 題庫治理、Markdown 母版、A4 Word 真雙欄與混合版面。v2.3.0 另支援既有成果的 `readable-revise`、A–L 可閱讀發布審查與可選工程學習 Profile。

## 重要邊界
這是一套 **Agent/LLM workflow + deterministic publishing/audit scripts**。Python scripts 不會自行理解原始教材、也不會偷偷摘要 PDF；來源閱讀、知識建模與語意忠實度必須由可讀取來源的 Agent/人工執行，scripts 負責結構、可追溯性、題數、Coverage、DOCX 與 release integrity。

## Codex repo 安裝
將資料夾命名為 `study-note-compiler`，放在 repository 的 `.agents/skills/`：

```text
.agents/skills/study-note-compiler/SKILL.md
```

使用 `$study-note-compiler` 明確呼叫；`ingest`、`model`、`build`、`compile`、`update`、`readable-revise`、`audit` 是 Skill 模式，不是 slash commands。

也可放入個人 skills 目錄供多個專案使用：

```text
~/.codex/skills/study-note-compiler/SKILL.md
```

## 常用模式

- `compile`：從正式來源建立完整、可追溯的學習筆記。
- `update`：只更新受新增資料影響的 KU、題目、Coverage 與索引。
- `readable-revise`：不重跑來源、不重建 KU，只微調既有筆記的學習閱讀層，並輸出 A–L 審查報告。
- `audit`：唯讀檢查，不修改成果。

工程／製程／系統整合主題可載入 `references/engineering_learning_profile.md`，建立「參數 → 機制 → 結果 → 量測 → 失效 → 性能／電性 → 良率／可靠度」與角色分工；其他學科不會被強制套用工程格式。

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
每個最終 DOCX：`python scripts/render_docx.py topic.docx --out-dir qa/topic → 每頁 PNG → 100% 視覺檢查 → 修正 → 重 render`。此 helper 使用 LibreOffice，或在 Windows 退回 Microsoft Word COM，並需要 Poppler `pdftoppm`；沒有 Render QA 就不能宣告完成。

## 公開使用與授權

程式、模板與 Skill 規則依 [MIT License](LICENSE) 公開，著作權人為 JYUN。使用者可依授權條款使用、修改與散布本 Skill。

本授權只涵蓋這個 Skill 套件本身，不會替輸入教材或生成筆記取得再散布權。公開筆記前仍須確認原始 PDF、投影片、圖片、題庫及引用內容的著作權與使用範圍；Skill 不會自動發布任何來源材料。
