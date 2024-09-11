from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from users.models import User  # 替换为你的应用名

class Command(BaseCommand):
    help = 'Generate fake users data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        for _ in range(total):
            # 随机生成教师或学生身份
            is_student = fake.boolean()
            is_teacher = not is_student

            # 随机生成第三方URL，50%几率为空
            third_party = fake.url() if fake.boolean() else None

            # 创建用户
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',  # 设置一个默认密码
                is_student=is_student,
                is_teacher=is_teacher,
                third_party=third_party,
                name=fake.name()
            )

            # 确保 last_login 不为空
            user.last_login = timezone.now()
            user.save()

            # 打印创建的用户信息
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} users'))