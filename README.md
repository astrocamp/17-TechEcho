# TechEcho

## 安裝步驟

1. `poetry shell` 虛擬環境
2. `poetry install` 下載 python 相應套件
3. `npm install` 下載 html/css/js 相應套件
4. 使用`.env.example` 建立`.env`檔

## 執行檔案

1. `npm run dev` 執行 esbuild 和 tailwind 除屑
2. `make server` 開啟伺服器

## 包含套件

1. CSS: tailwind, daisyUI
2. JS: alpine
3. Python: django, django-extensions, pre-commit, commitizen, python-dotenv

## Git push 步驟

1. make lint
2. git status
3. git add .........
4. make commit
5. git push -u origin <local>:<remote> (git push)
