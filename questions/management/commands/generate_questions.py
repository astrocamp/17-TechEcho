import random
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User
from questions.models import Question

class Command(BaseCommand):
    help = "生成指定數量的獨特技術問題，類似於 Stack Overflow 上的問題"

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', type=int, default=10,
            help="指定要生成的獨特技術問題數量"
        )

    def handle(self, *args, **kwargs):
        fake = Faker("zh_TW")
        users = User.objects.all()  # 不再限制為 is_student=True 的用戶
        question_count = kwargs['number']

        if not users.exists():
            self.stdout.write(self.style.ERROR("資料庫中未找到用戶。"))
            return

        technical_questions = [
            "如何在 Python 中處理多線程？",
            "Django 中如何使用自訂管理命令？",
            "請解釋 JavaScript 中的閉包概念。",
            "如何優化 SQL 查詢以提高性能？",
            "在 React 中如何使用 Hooks 管理狀態？",
            "什麼是面向對象編程的四大基本原則？",
            "請說明 Python 中生成器的工作原理。",
            "如何在 Linux 上配置 Nginx 作為反向代理伺服器？",
            "在 Git 中如何解決衝突並合併分支？",
            "RESTful API 和 GraphQL 有什麼區別？",
            "如何使用 Docker 管理容器？",
            "怎樣在 Java 中實現接口？",
            "Python 中的裝飾器是如何工作的？",
            "如何在 Django 中使用非同步視圖？",
            "JavaScript 中的事件冒泡是什麼？",
            "如何進行 Web 性能優化？",
            "什麼是 Lambda 表達式？",
            "如何在 SQL 中創建索引？",
            "Django 的 QuerySet 中的 `select_related` 和 `prefetch_related` 有什麼區別？",
            "如何在 Kubernetes 中部署應用程式？",
            "如何在 Vue.js 中處理組件間的通信？",
            "Python 中的上下文管理器是什麼？",
            "如何在 JavaScript 中使用 async/await？",
            "如何設置 PostgreSQL 資料庫的備份和恢復？",
            "在 Git 中如何查看提交歷史？",
            "如何在 Django 中進行表單驗證？",
            "什麼是 HTTP 快取？",
            "如何在 Swift 中處理異常？",
            "如何在 Android 中進行網絡請求？",
            "在 PHP 中如何處理會話？",
            "什麼是設計模式中的單例模式？",
            "如何在 JavaScript 中使用正則表達式？",
            "如何在 Node.js 中使用 Express 框架？",
            "什麼是 WebSocket，如何使用它？",
            "如何在 MongoDB 中執行複雜查詢？",
            "如何優化前端 JavaScript 性能？",
            "Django 中的中介軟體是什麼？",
            "如何在 Python 中使用多進程？",
            "如何在 React 中進行狀態管理？",
            "在 TypeScript 中如何定義接口？",
            "如何在 Linux 中查看系統日誌？",
            "什麼是 HTTPS，為什麼要使用它？",
            "如何在 Django 中實現用戶認證？",
            "如何處理大資料集的性能問題？",
            "什麼是資料可視化，如何實現？",
            "如何使用 Python 進行資料分析？",
            "什麼是微服務架構？",
            "如何在 Vue.js 中實現路由功能？",
            "在 C++ 中如何實現多態？",
            "如何在 Ruby on Rails 中處理文件上傳？",
            "如何在 Angular 中創建服務？",
            "如何在 Java 中實現多線程？",
            "什麼是資料建模？",
            "如何使用 SQL 進行資料聚合？",
            "如何在 Docker 中創建自訂鏡像？",
            "如何在 Python 中處理 JSON 資料？",
            "如何在 Git 中管理分支？",
            "什麼是 REST API？",
            "如何在 Node.js 中實現身份驗證？",
            "如何在 Django 中使用快取？",
            "如何在 JavaScript 中進行異步編程？",
            "如何在 Swift 中創建用戶介面？",
            "如何在 PHP 中處理表單資料？",
            "什麼是虛擬環境，如何使用？",
            "如何在 MySQL 中創建用戶權限？",
            "如何在 Django 中實現分頁？",
            "如何在 Kubernetes 中管理配置？",
            "如何在 Android 中實現持久化儲存？",
            "什麼是函數式編程？",
            "如何在 JavaScript 中使用 Promise？",
            "如何在 Django 中執行資料庫遷移？",
            "如何在 Python 中使用正則表達式？",
            "如何在 React 中進行組件優化？",
            "如何在 Vue.js 中使用指令？",
            "什麼是依賴注入？",
            "如何在 SQL 中使用事務？",
            "如何在 Java 中進行單元測試？",
            "如何在 Linux 中進行文件權限管理？",
            "如何在 Python 中進行性能調優？",
            "如何在 Docker 中進行網絡配置？",
            "如何在 PostgreSQL 中執行全文搜索？",
            "如何在 Django 中處理跨站請求偽造（CSRF）？",
            "如何在 Vue.js 中實現動態組件？",
            "如何在 Git 中使用標籤？",
            "什麼是依賴管理，如何使用工具？",
            "如何在 Android 中進行 UI 測試？",
            "如何在 PHP 中進行異常處理？",
            "如何在 JavaScript 中進行性能優化？",
            "如何在 Ruby 中實現元編程？",
            "什麼是 API 設計的最佳實踐？",
            "如何在 MongoDB 中管理索引？",
            "如何在 Swift 中使用 Core Data？",
            "如何在 Angular 中實現資料綁定？",
            "如何在 Django 中使用 Celery 進行異步任務？",
            "如何在 Python 中使用線程？",
            "如何在 Java 中使用註解？",
            "如何在 PHP 中處理 XML 資料？",
            "如何在 Docker 中配置多容器應用？",
            "如何在 Linux 中進行軟體包管理？",
            "如何在 JavaScript 中處理 DOM 操作？",
            "如何在 Django 中使用信號？",
            "如何在 Ruby on Rails 中處理後台作業？",
            "如何在 PostgreSQL 中優化查詢性能？",
            "如何在 Swift 中實現協議？",
            "如何在 Vue.js 中處理事件？",
            "如何在 Angular 中進行單元測試？",
            "如何在 Java 中進行網絡編程？",
            "如何在 Python 中使用資料庫連接池？",
            "如何在 Kubernetes 中進行服務發現？",
            "如何在 React 中使用上下文管理？",
            "如何在 PHP 中進行資料驗證？",
            "如何在 Django 中處理文件上傳？",
            "如何在 Linux 中進行系統監控？",
            "如何在 MongoDB 中使用聚合框架？",
            "如何在 Swift 中進行性能優化？",
            "如何在 Node.js 中處理異步操作？",
            "如何在 Vue.js 中實現動畫效果？",
            "如何在 Angular 中使用 RxJS 處理異步資料？",
            "如何在 Java 中使用反射？",
        ]

        if question_count > len(technical_questions):
            self.stdout.write(self.style.ERROR(f"無法生成 {question_count} 個獨特問題，只能生成 {len(technical_questions)} 個獨特問題。"))
            return

        generated_titles = set()
        created_count = 0

        while created_count < question_count:
            user = random.choice(users)  # 隨機選擇一個用戶
            title = random.choice(technical_questions)
            while title in generated_titles:
                title = random.choice(technical_questions)
            generated_titles.add(title)

            # 隨機生成 votes_count、answers_count 和 follows_count
            votes_count = random.randint(0, 3)
            answers_count = random.randint(0, 3)
            follows_count = random.randint(0, 3)

            question = Question.objects.create(
                title=title,
                details=fake.text(max_nb_chars=200),
                user=user,
                votes_count=votes_count,  # 確保 Question 模型中有這個字段

                answers_count=answers_count,  # 確保 Question 模型中有這個字段
                follows_count=follows_count  # 確保 Question 模型中有這個字段
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"已創建問題：{title}"))

        self.stdout.write(self.style.SUCCESS(f"成功創建 {created_count} 個問題。"))