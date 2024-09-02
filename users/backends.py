from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:

            user = User.objects.filter(username=username, email=email).first()
        except User.DoesNotExist:
            return None

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
