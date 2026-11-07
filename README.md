
# Campus FAQ AI Semantic Search System

校園 FAQ AI 智慧語意搜尋系統

## 專案介紹

本專案使用 Python、Ollama 與 Embedding 技術，
協助學生透過自然語言搜尋校園常見問題。

即使使用者的提問與資料庫問題用字不同，
系統仍可以透過語意相似度找出相關 FAQ。

## 主要功能

1. 校園 FAQ 語意搜尋
2. 支援同一問題的不同問法
3. 使用餘弦相似度排序搜尋結果
4. 顯示前三筆相關 FAQ
5. 相似度低於設定門檻時拒絕回答
6. 顯示 FAQ 答案與資料來源

## 使用技術

- Python 3.12
- uv
- Ollama
- qwen3-embedding:0.6b
- JSON
- GitHub Actions
- GitHub Pages

## 執行方式

1. 安裝 Python、uv 和 Ollama。
2. 下載 Embedding 模型：

   ollama pull qwen3-embedding:0.6b

3. 安裝專案依賴：

   uv sync

4. 執行程式：

   uv run python main.py

5. 輸入校園相關問題，查看搜尋結果。

## 專案架構

- main.py：主要 Python 程式
- faq.json：校園 FAQ 資料
- pyproject.toml：專案設定
- uv.lock：套件版本紀錄
- .gitignore：排除不應上傳的檔案

## AI 使用說明

本專案使用 Ollama 的 Embedding 模型，
將使用者問題及 FAQ 轉換為語意向量。

Python 計算餘弦相似度，依相關程度排序，
並顯示既有 FAQ 答案。

程式開發過程使用 ChatGPT 協助：
- 規劃系統架構
- 撰寫與修改程式碼
- 排除 Python 錯誤
- 設計搜尋測試

開發者自行執行程式、測試搜尋結果，
並依測試結果調整 FAQ 內容及搜尋邏輯。

## 注意事項

目前為課堂專題原型，FAQ 資料量有限。
相似度不等於答案正確率。
校園規定與申請流程請以學校最新公告為準。

## AI 語意搜尋測試結果

本專案使用 qwen3-embedding:0.6b 模型進行測試。

| 測試問題 | 搜尋結果 | 相似度 |
|---|---|---|
| 我的卡片掉了，還能重新申請一張嗎？ | 學生證遺失 | 68.85% |
| 我想取消這學期修的一門課 | 選課與加退選 | 72.60% |
| 我連不上學校的無線網路 | 校園 Wi-Fi | 92.92% |
| 我忘記學校系統的登入資訊了 | 密碼重設 | 91.34% |

### 測試發現

1. Embedding 能找到不同文字描述的相關 FAQ。
2. 部分問題相似度較低，可能受到門檻影響。
3. 一般退選與特殊退選等相近情境，仍可能產生搜尋歧義。
4. 語意相似度不代表答案正確率。
5. 系統目前使用 0.65 作為暫定搜尋門檻，尚未經完整測試集驗證。

## 專案連結

- GitHub Repository：https://github.com/Heyan0104/campus-faq-ai
- GitHub Pages：https://heyan0104.github.io/campus-faq-ai/