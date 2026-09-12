<!-- columns: 2 -->
# 10｜製程整合工程師示範筆記
適用：v2.3.0 學習閱讀版、真雙欄、A4 與嚴格 Gate QA
來源：SYNTHETIC_LAYOUT_FIXTURE（只用於 Skill 測試，不代表真實教材）

> **核心主軸**：製程整合不是看到一個異常參數就判根因，而是依「問題定義 → 圍堵 → 範圍 → 跨層資料 → 假設 → 驗證 → CAPA → 有效性追蹤」建立可驗證的工程閉環。

**【必背關鍵字】** Problem Definition、Containment、Scope、Commonality、Correlation、Causality、Root Cause、Verification、CAPA

**【先翻順序】** 角色定位 → 問題定義 → 風險圍堵 → 資料鏈 → Commonality → Hypothesis → Verification → Closure

## A｜專業重點筆記

### 先建立本章大圖
製程整合位在單站製程與產品結果之間：上游提供材料、圖形與結構狀態，中間由各模組完成轉換，下游則透過 Inline、WAT、CP、FT 與可靠度觀察結果。整合工程師的任務不是替每個模組調機，而是把跨站資料接成可驗證的影響路徑，先確認異常、界定風險，再找出最有區辨力的量測。若只盯著單一參數或單一站點，最容易把相關性誤當根因，也可能讓真正的良率或可靠度風險繼續流動。

<!-- ku: KU_PROBLEM -->
### 1. 「良率下降」還不是一個能處理的問題
看到 yield drop 時，第一步不是立刻安排 DOE，而是把模糊現象縮成可量測的問題：哪個產品與批次、從什麼時間開始、集中在哪些 wafer 或 fail bin、幅度多大，以及是否具有固定的空間或時間 signature。這些邊界共同形成 Scope，也決定後續該收哪些 Inline、WAT、CP、FT、設備歷史與材料資料。

在把異常歸因於製程前，還要先 Verify Abnormality。Tester、probe card、program 或 data mapping 都可能製造「看起來像製程異常」的假象。若量測系統尚未排除，後面的 commonality 和 DOE 即使出現差異，也未必對應真正失效。

常見誤判是把「良率下降」直接寫成問題定義。能進入工程分析的描述至少要交代對象、時間、失效 signature 與影響幅度；否則團隊甚至無法判斷兩筆資料是否在處理同一件事。

### 2. 標準工程處理流程
1. Define Problem：界定產品、批次、時間、失效型態與幅度。
2. Verify Abnormality：排除測試、資料、量測與系統假異常。
3. Containment：先阻止風險擴大，但不把圍堵誤認成根因。
4. Scope：縮小工具、腔體、材料、時間窗與產品範圍。
5. Data Collection：串起 Inline、WAT、CP、FT 與設備歷史。
6. Commonality：比較 good lots 與 bad lots 的共同條件。
7. Hypothesis：建立可被證偽的工程假設。
8. Verification：用加測、FA、split lot 或 DOE 驗證。
9. Root Cause：證據支持機制、時間順序與可重現性。
10. CAPA：修正原因並建立預防控制。
11. Effectiveness Monitoring：追蹤多批與可靠度，確認改善持續。
12. Closure：風險解除且文件更新後才正式結案。

<!-- ku: KU_COMMONALITY -->
### 3. Commonality｜Relationships / Application
Commonality 的目的不是找出「大家都有什麼」就宣布根因，而是把大量可能來源縮成少數可驗證假設。要同時看 good lots；若 good lots 也大量經過同一 tool，單純 tool commonality 的證據強度就下降。

應比較：tool / chamber、recipe、material、time window、mask/reticle、metrology/test、product/design 等條件。

**Pitfall**：Bad lots 都來自同一 chamber 只代表可疑，仍要比較 good lots、PM 時間線與後續驗證。

<!-- ku: KU_CAUSALITY -->
### 4. Correlation → Causality → Root Cause
- **Correlation**：兩個變數共同改變，只能提供線索。
- **Causality**：有合理機制與時間順序，可以解釋影響路徑。
- **Root Cause**：除了機制與資料，還要能以驗證與改善 response 支持，且最好可重現。

工程證據鏈：Correlation → Mechanism → Temporal Order → Testable Hypothesis → Verification → Corrective Response → Root Cause。

**Pitfall**：高相關係數、同一機台、或一次 recipe 修改後 yield 回升，都不能單獨證明根因。

### 5. Inline / WAT / CP / FT 因果資料鏈
Inline 偏幾何與物理製程量；WAT 偏結構電性；CP 是 die-level 功能與電性；FT 再加入封裝、socket、handler、溫度與 board-level 影響。四者不是互相取代，而是沿產品流程提供不同層次證據。

若 Inline → WAT → CP 的變化方向能被同一機制解釋，證據強度通常高於只有單一站點異常；若 FT 尚缺資料，則必須明確標示限制，不能假裝終端風險已關閉。

<!-- ku: KU_CLOSURE -->
### 6. Verification / CAPA / Closure
Verification 的任務是挑戰 Hypothesis。Corrective Action 修正已確認原因；Preventive Action 把學到的機制更新到 OCAP、FMEA、Control Plan 或 SOP；Effectiveness Monitoring 再確認改善能跨批次持續。

**Pitfall**：Hold lot 是止血，不是 diagnosis；yield recovery 是好訊號，但不是 Closure。

### 7. 快速辨析
| 情境 | 不能直接下的結論 | 正確下一步 |
|---|---|---|
| WAT 尾端變差但 CP 尚正常 | 產品一定沒問題 | 看 margin、趨勢、可靠度與製程共同性 |
| Bad lots 都經過同一 tool | tool 已確定是根因 | 比較 good lots、時間窗、chamber 與驗證結果 |
| 兩參數高度相關 | 已證明因果 | 建立機制、時間順序與驗證計畫 |

### 8. 本章快速複習
★ Hold lot 是止血，不是診斷。Commonality 是縮小範圍，不是 root cause。Correlation 是線索，不是因果。真正結案還要有驗證、改善持續性、風險解除與文件更新。

## B｜L1–L2 基礎與解釋題（10 題）
題目 1：問題定義至少要固定哪三類邊界？
答：至少固定產品/批次、時間窗與失效型態；工程上還應補站點、工具、腔體或材料等範圍。

題目 2：Commonality Analysis 的基本比較對象是什麼？
答：比較 good lots 與 bad lots 的工具、腔體、材料、recipe、時間與量測共同條件。

題目 3：Correlation 與 Causality 最基本的差異是什麼？
答：Correlation 只表示共同變動；Causality 還需要合理機制與時間順序支持影響路徑。

題目 4：Containment 與 Corrective Action 有何差異？
答：Containment 先阻止風險擴大；Corrective Action 則針對已確認原因進行修正。

題目 5：正式 Closure 前還要確認什麼？
答：要確認改善持續有效、風險解除、可靠度與其他產品沒有新增風險，並完成制度文件更新。

題目 6：為什麼 Problem Definition 應先於 DOE？
答：因為 scope 與 response 未固定時，DOE 容易混入無關因素，結果即使有差異也難以解釋。

題目 7：為什麼 Commonality 不能直接等同 Root Cause？
答：共同性只縮小可疑來源，仍需要機制、時間順序與受控驗證才能升級成根因。

題目 8：從 Correlation 到 Root Cause 還缺哪些證據？
答：至少要補物理或工程機制、時間順序、可證偽假設與受控驗證，並觀察修正後問題是否下降。

題目 9：Preventive Action 為什麼不是單純重做 Corrective Action？
答：Preventive Action 是把已知機制制度化，降低同類問題在其他批次、產品或未來條件再次發生的機率。

題目 10：為什麼 yield recovery 不等於可以立即結案？
答：短期回升可能只是波動；仍需 effectiveness monitoring、可靠度檢查與制度更新才能證明改善可持續。

## C｜L3–L4 情境與診斷題（10 題）
題目 11：只有 CP fail bin 與 wafer map 時，下一步最值得補哪三類資料？
答：優先補製程/設備歷史、WAT/Inline 對應資料與時間/工具/腔體共同性，讓失效 signature 能回接製程流程。

題目 12：所有 bad lots 都經過同一 chamber，下一步怎麼做？
答：先查 good lots 是否也經過該 chamber，再比 PM、recipe、時間窗與其他腔體，最後設計驗證而非直接判根因。

題目 13：某製程參數與 leakage 高度相關，如何設計下一步？
答：先確認參數變化早於失效且存在合理機制，再用 split lot、DOE 或受控加測改變該參數並觀察 leakage response。

題目 14：recipe 修改後 yield 回升，還要做什麼？
答：追蹤多批、檢查可靠度與其他產品，確認改善持續性，再更新 OCAP/FMEA/Control Plan/SOP。

題目 15：產品仍 pass 規格但分布向邊界偏移，應怎麼處理？
答：不能只看 pass rate；應比歷史分布與 margin，串接製程資料與可靠度風險，再判斷是否加測或圍堵。

題目 16：Bad lots 與某材料批次完全重疊，為何仍可能不是材料根因？
答：材料批次可能同時綁定特定機台或時間窗；必須用 good lots、其他材料批次與受控驗證排除共變因子。

題目 17：一次把參數調回正常後良率恢復，足以證明根因嗎？
答：不足。還要確認機制、時間順序與可重現性，最好用對照或再次受控改變建立反事實證據。

題目 18：Hold lot 後未再出現不良，可以結案嗎？
答：不可以。Hold lot 只阻斷暴露，沒有證明原因消失；仍需根因驗證、改善、有效性追蹤與風險解除。

題目 19：良率突然下降但所有製程參數正常，最危險的第一個假設是什麼？
答：要先排除 tester、probe card、program、資料 mapping 或量測系統假異常，避免把量測問題誤導成製程根因。

題目 20：若 Inline 異常、WAT 輕微偏移、CP fail 明顯但 FT 樣本不足，如何判斷證據強度？
答：可視為跨層一致的因果線索，但 FT 與可靠度證據仍不足；應明確標示限制並補終端或可靠度驗證。

## D｜Active Recall / Feynman
- 不看筆記，完整說明「Commonality → Hypothesis → Verification」為什麼不能少任何一段。
- 用一般人能理解的方式解釋「Correlation 不等於 Causality」。
- 假設只有 CP fail bin 與 wafer map，列出下一批最值得補收的三類資料，並說明每一類能排除什麼假設。
- 用 30 秒說明為什麼「yield recovery ≠ closure」。

<!-- columns: 1 -->
## Coverage Matrix
| Knowledge Unit | Source | Note | L1/L2 | L3/L4 | Pitfall | Status |
|---|---|---|---|---|---|---|
| KU_PROBLEM｜Problem Definition / Scope | synthetic | ✓ | ✓ | ✓ | ✓ | PASS |
| KU_COMMONALITY｜Commonality | synthetic | ✓ | ✓ | ✓ | ✓ | PASS |
| KU_CAUSALITY｜Correlation / Causality / Root Cause | synthetic | ✓ | ✓ | ✓ | ✓ | PASS |
| KU_CLOSURE｜Verification / CAPA / Closure | synthetic | ✓ | ✓ | ✓ | ✓ | PASS |
