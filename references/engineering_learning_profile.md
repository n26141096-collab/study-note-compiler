# Engineering Learning Profile

## 何時使用

使用者要建立工程製程、設備、實驗、故障診斷、製造或系統整合筆記時，於通用 learner-facing 規則之外載入本 profile。

這是可選的學科 profile，不應套用到所有人文、法規或語言學習筆記。

## 章首大圖

工程章節在進入細節前，優先回答：

1. 這個模組／站點／方法在整體系統中做什麼？
2. 它位於哪個 upstream → current → downstream 關係？
3. 工程師能控制的主要輸入是什麼？
4. 交給下游的主要輸出是什麼？
5. 哪個量測最早看得到結果？
6. 出錯時可能影響哪個結構、性能、可靠度或產出？

控制在約半頁到一頁。來源不足的節點保留 `SOURCE_NOT_FOUND`，不得補成看似完整的因果鏈。

## 核心工程鏈

依來源可支持範圍建立：

`Controllable Parameter → Physical Mechanism → Process/System Result → Measurement → Failure/Defect → Downstream Structure → Performance/Electrical → Yield/Reliability`

先用完整句子解釋，再用箭頭作高密度摘要。不是每個 KU 都必須畫完整鏈。

## 角色分流

當學習目標包含不同工程角色時，依實際責任分流，不只換標題：

- **局部 owner 視角**：parameter、recipe、equipment、process window、monitor、drift、maintenance、experiment。
- **整合 owner 視角**：upstream/downstream、interface、cross-module、system response、qualification、performance、yield/reliability。

角色名稱由使用者領域決定。半導體製造可使用 PE／PI；其他領域不得硬套 PE／PI。

## 高階異常處理

適用時建立：

`Confirm → Scope → Containment → Commonality → Process/System Data → Equipment Data → Upstream/Downstream → Hypothesis → Verification → Root Cause → Corrective Action → Preventive Action → Release/Monitoring`

這是問題拆解順序，不是來源替代品。實際 control limit、hold/release、OCAP、DOE 範圍或 qualification 規範必須來自正式來源或使用者提供的制度。

## Commonality

依領域選擇能區分 good／bad 的 exposure 維度，例如：

- batch／lot／sample；
- product／design／layer；
- tool／chamber／fixture；
- recipe／method／software version；
- time／shift／maintenance；
- material／consumable／operator；
- upstream condition／downstream result。

Commonality 只能排序假設。Root cause 還需要時間順序、物理可行性、good/bad 分離、獨立驗證與修正後回復。

## L3–L4 工程題

案例應提供不完整但可推理的資訊，讓學習者決定下一步：

- 已知症狀與 baseline；
- 至少兩個競爭假設；
- 一部分正常、一部分異常資料；
- 可選的量測或驗證；
- 結論邊界。

答案依「先確認 → 界定範圍 → 分流假設 → 補收證據 → 判斷是否足以結案」組織。不要每題都問「如果你是某角色會怎麼做」。

## 工程總覽文件

當主題多於數章且跨模組關係重要時，建立一份 mental model，至少連接：

`Requirement/Design → Process/System Flow → Unit Operation → Inline/Intermediate Measurement → Final Test → Performance/Yield → Reliability`

這份總覽是導航，不重新摘要所有章節。
