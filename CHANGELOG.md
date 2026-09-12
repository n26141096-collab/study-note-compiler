# Changelog

## 2.3.0 — 2026-09-01
- 新增 `$study-note-compiler readable-revise`，在不重跑來源、不重建 KU 的前提下修訂既有學習閱讀層。
- 新增唯讀 `$study-note-compiler audit` 模式。
- 新增 A–L 可閱讀發布審查、85/80 分門檻、Hard Blocker 與 governance sidecar hash 非回歸驗證。
- 新增章首「本章大圖」規格與可選工程學習 Profile，補強工程因果鏈、角色分工、問題拆解與情境題品質。
- 新增 `READABLE_RELEASE_GATE`、可閱讀修訂報告模板與相應 content rules。
- 新增 MIT License（Copyright 2026 JYUN）與 Codex `agents/openai.yaml` 公開介面。
- 更新 SKILL、README、模板與學習者正文規格；既有 FAB 筆記不在本次修改範圍。

## 2.2.0 — 2026-09-01
- 將八層 Knowledge Unit 明確限定為 sidecar 完整性模型，不再要求正文逐欄顯示。
- 新增來源稽核層／學習閱讀層，完整 locator 留在 YAML，正文改用人類可讀短來源。
- 新增 learner-facing 寫作規格與自然工程敘事範例。
- 新增 `learner_facing_audit.py`，拒絕固定標籤網格、跨 KU 後設長句、複製題幹與 raw archive locator。
- 新增 `TEMPLATE_REPETITION_GATE`、`LEARNER_FACING_GATE` 與人工 `READABILITY_GATE`。
- 更新主題模板、content rules、schema、README 與對抗測試。

## 2.1.1 — 2026-09-01
- 修正 SKILL frontmatter：版本移至 `metadata.version`。
- 呼叫方式改為 `$study-note-compiler <mode>`，移除偽 slash command 表述。
- Coverage Gate 強制 KU 集合完整、唯一且無未知項目。
- Source Locator Gate 強制每個重大 KU 與每道題都有 locator。
- Markdown 新增 KU marker 與實質內容 Gate，關鍵詞空殼不得通過。
- Release Manifest Gate 拒絕未列入清單的額外檔案。
- 新增跨平台 LibreOffice/Poppler render helper 與對抗測試。

## 2.1.0 — 2026-09-01
- Hard fix：真正寫入 A4 210 × 297 mm，continuous sections 保持相同 page geometry。
- Font fix：East-Asian 與 Latin font slots 分開設定。
- Source governance：新增結構化 source locator，正式 release 禁止 synthetic locator。
- Coverage fix：status 完全由程式計算，手填 `status` / `computed_status` 直接 FAIL。
- Professional Note Gate：加入 100 分機械 Rubric 與 hard blockers。
- Assessment gate：正式主題至少 L1/L2 10 題、L3/L4 10 題。
- Validator：topic 與 master index profile 分離；DOCX 結構 Gate 加入 A4 實體頁面檢查。
- Packaging：新增 `requirements.txt`、release manifest builder/auditor。
- Tests：加入 A4、假關鍵字筆記、假 PASS coverage、source locator、master-index regression tests。

## 2.0.0
- Knowledge Modeling-first、Coverage-driven 題庫、真雙欄與 mixed layout。
