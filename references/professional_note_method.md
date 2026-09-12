# Professional Note Method

## 參考架構（只吸收方法，不複製程式碼或文字）

### Renakoni/note-organizer
可借鑑：
- 先掃描資料角色，再推斷章節。
- 優先抽取既有題目。
- 建立來源索引、資料缺口、題目覆蓋檢查。
- 長課程採增量更新，不每次全量重做。
來源：https://github.com/Renakoni/note-organizer

### claude-code-best/claude-code — teach-me
可借鑑：
- 筆記先回答 What / Why，再到 How。
- 每節以 one-line summary + 短解釋 + example / cheat sheet 呈現。
- 筆記是「學習者回顧用」，不是聊天逐字稿。
來源：https://github.com/claude-code-best/claude-code/blob/main/.claude/skills/teach-me/SKILL.md

### SkillMedev/personal-operating-system — study-system
可借鑑：
- 把課程拆成可測試知識原子。
- 以 Active Recall 取代只重讀。
- 使用 Feynman prompt 找出理解缺口。
- 使用 spaced repetition 與 error log。
來源：https://github.com/SkillMedev/personal-operating-system/blob/main/skills/study-system/SKILL.md

## 本 Skill 的組合方式
本 Skill 不直接複製上述專案；只抽象出三類方法：
1. Source/Question Governance
2. Knowledge Modeling + 自然學習敘事
3. Retrieval Practice + Coverage Audit

再加入本 Skill 自己的 Markdown → Word 真雙欄出版層。

## v2.2 寫作分層

What／Why／How 是建模檢查清單，不是固定排版欄位。完整八層 KU 保存在 YAML；學習正文依內容選擇最自然的入口，例如問題、現象、比較、流程、反例或工程情境。正文應能離開 sidecar 單獨閱讀，但不得失去 sidecar 的來源映射。

當模板與可讀性衝突時，保留模型完整性，改寫可見呈現。不要刪除來源、關係或 pitfall；應把它們融入最接近的解釋或判斷段落。
