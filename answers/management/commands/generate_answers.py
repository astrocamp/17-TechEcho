import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from questions.models import Question
from answers.models import Answer, Vote
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "生成假資料：為每個問題生成多個中文答案與對應的投票"

    def handle(self, *args, **kwargs):
        fake = Faker("zh_TW")

        # 獲取所有的問題
        questions = Question.objects.all()
        if not questions:
            self.stdout.write(self.style.ERROR("沒有可用的問題"))
            return

        # 獲取所有的使用者，並過濾出 is_teacher 為 True 的使用者
        teachers = User.objects.filter(is_teacher=True)
        if not teachers:
            self.stdout.write(self.style.ERROR("沒有教師使用者"))
            return

        # 確保每個教師使用者都有至少兩個答案
        teacher_answers = {teacher: [] for teacher in teachers}
        for teacher in teachers:
            # 設置 last_login 為當前時間
            teacher.last_login = timezone.now()
            teacher.save()

            # 每個教師生成 2 到 5 個答案
            num_answers = random.randint(2, 5)
            for _ in range(num_answers):
                # 隨機選擇一個問題來生成答案
                question = random.choice(questions)
                answer_content = fake.sentence(nb_words=20)  # 繁體中文且不換行
                answer = Answer.objects.create(
                    question=question,
                    content=answer_content,
                    user=teacher,
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                )
                teacher_answers[teacher].append(answer)

                # 生成0到5個投票
                num_votes = random.randint(0, 5)
                for _ in range(num_votes):
                    voter = random.choice(User.objects.exclude(id=teacher.id))
                    vote_type = random.choice(["upvote", "downvote"])
                    Vote.objects.get_or_create(
                        user=voter,
                        answer=answer,
                        defaults={"vote_type": vote_type},
                    )

        self.stdout.write(self.style.SUCCESS("教師使用者的假資料生成完畢"))

        # 生成每個問題的其他答案
        for question in questions:
            # 確保問題有 1 到 5 個答案，其中一些來自教師
            existing_answers = Answer.objects.filter(question=question)
            num_answers = max(
                1, 5 - existing_answers.count()
            )  # 確保每個問題至少有 1 個答案
            for _ in range(num_answers):
                answer_content = fake.sentence(nb_words=20)  # 繁體中文且不換行
                answer = Answer.objects.create(
                    question=question,
                    content=answer_content,
                    user=random.choice(
                        User.objects.exclude(
                            id__in=[teacher.id for teacher in teachers]
                        )
                    ),
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                )

                # 生成0到5個投票
                num_votes = random.randint(0, 5)
                for _ in range(num_votes):
                    user = random.choice(
                        User.objects.exclude(
                            id__in=[answer.user.id for answer in existing_answers]
                        )
                    )
                    vote_type = random.choice(["upvote", "downvote"])
                    Vote.objects.get_or_create(
                        user=user,
                        answer=answer,
                        defaults={"vote_type": vote_type},
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"已為問題 '{question}' 生成額外的答案及對應的投票資料"
                )
            )

        self.stdout.write(self.style.SUCCESS("假資料生成完畢"))
