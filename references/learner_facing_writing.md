# Learner-facing Writing Standard

## 目的

把來源受控的 Knowledge Unit 編寫成真正能讀、能講、能用來判斷的學習正文。這份規格不放寬來源、Coverage 或題庫要求；它只規定 sidecar 資料如何轉成自然文字。

## 兩層輸出

### 來源稽核層

`knowledge_units.yaml`、`assessment.yaml`、`coverage.yaml` 保存完整八層 KU、完整 source locator、題目欄位與 evidence flags。這一層可以結構化、冗長，但必須可機械驗證。

### 學習閱讀層

Markdown／DOCX 是給人閱讀的版本。它保留 KU marker 供映射，但不顯示 YAML 欄位表。完整 archive path、hash filename、evidence 與 confidence 留在 sidecar；正文只在段尾或章末顯示教材名、講次、頁碼等短來源。

## 寫作原則

1. 章首先建立本章大圖：本章角色、在整套學習順序的位置、需要哪些前置概念或輸入、產生什麼輸出，以及錯誤或失敗會影響什麼。篇幅以半頁到一頁為原則，不要先堆名詞。
2. 再找出讀者真正要回答的問題，選擇問題導向、機制導向、比較導向、流程導向或案例導向的入口。
3. 一個 KU 通常使用 2–4 個有連續關係的短段落；不要求每段顯示 What、Why、How 等標籤。
4. 專有名詞保留必要英文，其餘使用自然中文。避免中英詞彙和箭頭鏈密集到中斷句意。
5. 因果鏈可以作為段末摘要，但前文必須先用完整句子解釋每個關係。
6. Pitfall 放在最接近誤判發生的位置；不要每節固定加一條泛用警語。
7. 不使用「本教材用來連結製程步驟、結構轉換與可量測結果的知識單元」等可套在任何主題的後設句。
8. 同章 KU 的句型、開頭與案例角度應隨內容改變，但不能為追求變化而改變來源意思。

## 工程類正文

只有主題確實屬於工程、製程或系統整合時，才套用 `engineering_learning_profile.md`；非工程主題不得硬塞 tool、yield、electrical 等欄位。

工程 KU 可依情況選擇：

- **症狀切入**：看到什麼異常 → 哪些模組可能造成 → 第一輪先量什麼 → 如何排除 → 哪些證據才能支持 root cause。
- **機制切入**：參數改變 → 物理機制 → 直接結果 → 缺陷／失效 → downstream／electrical／yield impact。
- **比較切入**：兩種條件的共同基準 → 關鍵差異 → 適用範圍 → 容易誤用的邊界。
- **流程切入**：目的 → 先後順序 → 每一步的控制點 → 失敗時的可觀察結果。

不要每個 KU 都硬套同一條鏈。鏈中的節點若來源沒有支援，標記來源邊界，不用模型常識補滿。

## L3–L4 題目與答案

情境題應改變觀察、限制與可用資料，而不是只替換 KU 名稱。答案優先包含：

1. 第一個要確認的觀察或量測。
2. 用來區分主要假設的分流方式。
3. 需要補收的物理、inline、electrical 或其他領域證據。
4. 哪些結果只能算 correlation，何時才足以支持結論。

## 前後對照

不佳：

> PE／PI Application：chamber A/B profile 不一致時，先比 pressure、bias/power 與 gas delivery。Pitfall：不能只比 recipe name。

較佳：

> 假設 Chamber A 的 CD 正常，Chamber B 卻持續偏小，先不要只比較兩台機台的 recipe 名稱。名稱相同不代表 wafer 實際承受的電漿條件相同。第一輪應確認 chamber pressure、bias power、source power 與 gas delivery 的實際 trace，再看差異是否伴隨側壁角度或底部損傷變化。若 CD 與 profile 同時改變，問題通常比單純量測偏差更接近電漿條件或腔體狀態。

## Readability Gate

每個主題至少抽查 3 個 KU：一個核心機制、一個應用／比較、一個高階診斷。逐段朗讀並確認：

- 不看 YAML 也能理解段落在回答什麼。
- 沒有連續的欄位填充感或可跨主題複製的後設句。
- 來源註記不打斷主要推理。
- 讀完能用自己的話重述判斷與邊界。
- L3–L4 不會只因替換名詞就變成另一題。

任一抽樣 KU 未通過，修正該主題後重新抽查；不得只在 Audit Report 勾選 PASS。

若審查對象是已完成編譯的整套筆記，改用 `readable-revise`，並依 `readable_revision.md` 完成 A–L 評分、Hard Blocker 檢查與治理 sidecar hash 驗證。此流程只修學習閱讀層，不重建來源與 Knowledge Unit。
