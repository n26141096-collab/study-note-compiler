# Professional Note Quality Rubric v2.3

滿分 100。此分數是「機械式可驗證品質 Gate」，用來檢查來源定位、知識建模、題庫覆蓋、檢索性與明顯缺陷；**不宣稱能自動證明教材內容的語意真偽**。語意是否忠於來源仍由來源感知的 Agent / 人工審查負責。

| 面向 | 權重 | 機械 Gate |
|---|---:|---|
| Source Fidelity | 20 | 重大 KU 與題目具結構化 source locator；file/locator/evidence/confidence 完整 |
| Knowledge Modeling | 20 | critical/high KU 的八層 sidecar 完整，且 Markdown 有唯一 KU marker 與至少 120 字元實質內容 |
| Relationships & Causality | 15 | 重大 KU 具實質 How + Relationships，不只定義堆疊 |
| Retrieval Usefulness | 15 | 核心主軸、關鍵字、先翻順序、本章快速複習／最後速背、Active Recall 可快速取得 |
| Assessment Quality | 15 | 正式主題至少 L1/L2 10 題 + L3/L4 10 題；題目綁 KU 與來源 |
| Pitfalls & Discrimination | 10 | 重大 KU 有可辨識的常見誤判/邊界 |
| Compression without Distortion | 5 | 無 placeholder，沒有明顯整段重複 |

上述 100 分仍是機械式品質分數。v2.3 另設四個不計分 Hard Gate：

| Gate | 驗收方式 |
|---|---|
| TEMPLATE_REPETITION_GATE | `learner_facing_audit.py` 檢查多數 KU 是否使用同一組可見標籤、跨 KU 長句重複、題幹是否只替換名詞 |
| LEARNER_FACING_GATE | 機械檢查正文不得暴露 archive internal path／hashed locator；人工確認正文先服務學習理解 |
| READABILITY_GATE | 每主題抽查至少 3 個 KU，朗讀並確認可自然解釋、段落銜接清楚、沒有資料庫輸出感 |
| READABLE_RELEASE_GATE | `readable-revise` 依 A–L 人工審查，平均至少 85 分且 governance sidecar hash 不變；細則見 `readable_revision.md` |

## Release threshold
- 90–100：RELEASE_READY
- 80–89：PASS_WITH_MINOR_FIXES
- 70–79：REWORK_REQUIRED
- <70：FAIL

## Hard blockers
- Source Fidelity < 16/20
- Knowledge Modeling < 16/20
- Formal assessment minimum 未達成
- Coverage 非全 PASS
- Coverage KU 集合不完整、重複或包含未知 KU
- Markdown 缺少重大 KU marker、marker 重複或 block 過薄
- 任一重大 KU 或題目缺少有效 source locator
- placeholder / 待補內容進入正式筆記
- Coverage status 由人工填寫而非程式計算
- 多數 KU 以相同 What／Why／How／Application／Pitfall 標籤逐欄輸出
- 正文直接傾倒 hashed source path 或 archive internal path
- 題庫大量複製同一題幹，只替換 KU 名稱
- 未完成抽樣人工 READABILITY_GATE 或抽查結果 FAIL
