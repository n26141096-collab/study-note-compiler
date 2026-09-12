# Readable Revision and Release Standard

## 適用時機

當筆記已完成來源解析、Knowledge Unit、題庫與 Coverage，但閱讀體驗仍像系統輸出時，使用 `$study-note-compiler readable-revise`。

這個模式只重新出版閱讀層，不是再次 compile。

## 不可變範圍

開始前記錄下列治理檔案的 SHA-256，完成後必須相同：

- `knowledge_units.yaml`
- `coverage.yaml`
- `coverage_computed.yaml`
- `source_registry.yaml`
- material roles 或同等來源分級檔

除非使用者明確要求修正知識或來源，禁止：

- 重新解析原始教材；
- 重建 Knowledge Unit；
- 改寫 source locator；
- 重建 Coverage 邏輯；
- 用模型知識填補來源缺口；
- 為了可讀性刪除題目、答案或 evidence lineage。

## 修訂順序

`Knowledge Integrity > Engineering/Domain Accuracy > Human Readability > Formatting Consistency`

`KEEP > MICRO_EDIT > LOCAL_REWRITE > RESTRUCTURE`

先保留已經正確好讀的段落，只修正真的阻礙學習之處。

## 閱讀層修訂

每章先建立大圖，再進細節。依學科選擇適用項目：

1. 本章或這個流程在整體中的角色。
2. 前置條件、輸入或已知假設。
3. 本章產生的輸出、判斷或能力。
4. 失敗、誤用或理解錯誤會影響什麼。
5. 第一次閱讀後應能說出的核心心智模型。

正文用概念、問題、機制、比較、流程或案例作為標題，不使用資料欄位作為固定標題。題目集中在題庫區；第一次閱讀正文只保留少量真正能促進理解的提問。

來源治理採雙層：

- 正文：教材名、章節／講次、頁碼等短來源。
- sidecar：完整檔名、archive path、locator、evidence、confidence。

## Readable Learning Edition Audit

修訂後依 A–L 評分，每項 0–100，並在 `READABLE_REVISION_REPORT.md` 寫出證據：

| 維度 | 審查內容 |
|---|---|
| A. 模板感 | 固定欄位、重複句型是否仍主導正文 |
| B. KU 可見程度 | 治理 marker 是否隱藏，讀者是否仍像在讀資料庫 |
| C. 正文連續閱讀性 | 是否先有大圖、短段落、自然順序與清楚轉場 |
| D. Raw locator | archive／hash locator 是否已移出閱讀層 |
| E. L3–L4 重複 | 題幹是否只替換名詞，案例資料是否真正不同 |
| F. 角色／用途分流 | 若學習目標含不同角色，責任與判斷尺度是否清楚 |
| G. 高階問題處理 | 是否包含確認、界定、驗證、修正與預防的閉環 |
| H. 比較／共同性 | 是否能用多維度資料區分競爭假設 |
| I. 關係與因果 | 是否把概念接到可觀察結果，而非只列名詞 |
| J. 快速複習 | 是否有高密度回想點，且沒有重抄正文 |
| K. Source traceability | 短來源與 sidecar 完整定位是否同時成立 |
| L. Technical integrity | 修訂是否保持原知識、公式、邊界與不確定性 |

總分採任務加權，但不得用高分掩蓋 Hard Gate：

- 85–100：`READABLE_RELEASE = PASS`
- 80–84：`READABLE_RELEASE = PASS_WITH_MINOR_REVISION`
- 0–79：`READABLE_RELEASE = NEEDS_REVISION`

以下任一失敗不得宣告 PASS：

- raw archive locator 不為 0；
- visible KU template 仍主導多數正文；
- L3–L4 大量複製同一題幹；
- source traceability 或 technical integrity 失敗；
- 人工 Readability Gate 未完成；
- 正式 DOCX 未完成逐頁 Render QA。

## 最終報告

報告至少包含：

- 修改的閱讀層檔案；
- 未變更治理檔案及前後 SHA-256；
- raw locator、模板標籤與重複題幹的前後統計；
- 人工抽查 KU 與結果；
- A–L 分數及理由；
- Word 結構與逐頁視覺 QA；
- 最終分數與 Release verdict。
