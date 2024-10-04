# TechEcho

找飯店？ Trivago
找答案？ Techecho
專案網址： https://www.tech-echo.dev

#### 功能說明
**1. 註冊登入：** 進入Techecho，若要發問、留言、發表技術文章請點擊註冊按鈕並登入。
![home](./static/images/首頁.png)
**2. 搜尋功能：** 搜尋關鍵字，可找出想要的問題、專家、部落格文章。
![search](./static/images/搜尋.png)
**3. 問題列表：** 可以看到使用者在網站上提出的所有問題
![問題列表](./static/images/問題列表.png)
**3. 成為專家：** 成為專家可以與學生一對一的教學互動，有自己的聊天室以及共編。
以及可以排定自己的上課行程。
**4. 成為Premium用戶：** 升級成Premium用戶可以預約專家，進行更深入的討論。
![chat](./static/images/聊天室.png)
**5. 部落格：** 發表技術文章。
![Blog](./static/images/文章列表.png)


## 使用技術

- 前端：daisyUI, TailwindCSS, Alpinejs, HTMX, Vue
- 後端：Python, Django
- 資料庫：PostgreSQL
- 版本控制：Git
- 第三方登入：Google, GitHub
- 上傳照片：S3
- 部署：AWS EC2, ALB, Route53, ACM, Nginx(Web Server)
- ASGI Server：Daphne
- 通道層、快取：Redis
- 執行使用者的程式碼、確保資料庫與快取的部署環境：Docker
- 規劃：Miro, Google Sheets

## 團隊成員

- 林永欣 / Alex [GitHub](https://github.com/alextechtrek)

  - 第三方登入
  - 串接 LINE pay 金流
  - 製作部落格功能

- 許修福 [GitHub](https://github.com/buding033171)

  - 專家頁面新增/編輯
  - 專家列表與篩選功能
  - 專家檔案與答題紀錄
  - 串接聊天室

- 陳威辰 / Will [GitHub](https://github.com/Double-T1)

  - 一對一聊天室
  - 製作文字編輯器
  - 問題功能
  - 通知小鈴鐺

- 紀祥文 / Chi [GitHub](https://github.com/chixxyy)

  - UI/UX 設計
  - 搜尋功能
  - 動畫製作
  - 追蹤專案進度

- 林倩瑜 / Eudora [GitHub](https://github.com/imEudora)

  - 製作回答功能
  - 老師教學時段安排
  - 學生預約系統

- 洪芷儀 / Sabina [GitHub](https://github.com/sabina726)

  - 會員登入註冊
  - 個人資料修改
  - 會員在網站的紀錄
  - 公開的個人頁面

- 李彥賜 / Tony [GitHub](https://github.com/buding033171)

  - 付款功能流程/資料庫設計
  - 串接整合第三方金流功能
  - 串接 AWS S3
  - 網站雲端部署




## 安裝環境

1. `poetry shell` 虛擬環境
2. `poetry install` 下載 python 相應套件
3. `npm install` 下載 html/css/js 相應套件
4. 使用`.env.example` 建立`.env`檔

## 執行環境

1. `docker compose up -d` 建立編輯器所需的 docker image, 以及架起 redis
2. `npm run dev` 執行 esbuild 和 tailwind 編譯
3. `make server` 開啟伺服器
