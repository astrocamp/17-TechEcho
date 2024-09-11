import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from teachers.models import Teacher


class Command(BaseCommand):
    help = "Generate fake data for Teacher model"

    def handle(self, *args, **kwargs):
        fake = Faker("zh_TW")
        User = get_user_model()

        programming_languages = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "C#",
            "Ruby",
            "Go",
            "Swift",
            "Kotlin",
            "PHP",
            "R",
            "Rust",
            "TypeScript",
            "Scala",
            "Perl",
        ]

        schedules = [
            "週一上午 9:00 - 11:00",
            "週二下午 2:00 - 4:00",
            "週三上午 10:00 - 12:00",
            "週四晚上 7:00 - 9:00",
            "週五下午 3:00 - 5:00",
            "週六上午 8:00 - 10:00",
            "週日下午 1:00 - 3:00",
        ]

        introduce_templates = [
            "我是{expertise}專家，擁有豐富的開發經驗和教學背景。",
            "作為{expertise}的專家，我致力於教授學生掌握該領域的關鍵技能。",
            "我有多年的{expertise}教學經驗，能幫助你快速入門並精通該語言。",
            "我的專長是{expertise}，我將幫助你深入理解並實踐這項技術。",
            "作為{expertise}領域的專家，我的教學方法實用且有效。",
            "我在{expertise}方面有多年的實戰經驗，將帶你從基礎到進階。",
            "我的{expertise}課程將幫助你掌握從理論到實踐的所有技能。",
            "學習{expertise}是一項挑戰，但我會幫助你輕鬆應對。",
            "我專注於{expertise}的實踐應用，讓你快速掌握該技術。",
            "作為{expertise}的資深開發者，我的教學內容將直擊重點。",
        ]

        teachers = User.objects.filter(is_teacher=True)
        for user in teachers:
            if not hasattr(user, "teacher"):
                # 隨機選擇 1 到 3 個程式語言
                selected_languages = random.sample(
                    programming_languages, random.randint(1, 3)
                )
                expertise = ", ".join(selected_languages)

                introduce = random.choice(introduce_templates).format(
                    expertise=expertise
                )

                # 生成三個字的姓名作為 nickname
                nickname = (
                    fake.last_name() + fake.first_name()[:1] + fake.first_name()[:1]
                )

                schedule = random.choice(schedules)

                Teacher.objects.create(
                    user=user,
                    expertise=expertise,
                    introduce=introduce,
                    nickname=nickname,
                    schedule=schedule,
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated fake data for Teacher model")
        )
