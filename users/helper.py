from django.core.mail import send_mail
from django.conf import settings 
from django.urls import reverse


def send_forget_password_mail(email, token):
    subject = '重設您的密碼'
    try:
        reset_url = reverse('users:change_password', kwargs={'token': token})
        message = f'您好，請點擊以下連結重設您的密碼：\n\nhttp://127.0.0.1:8000{reset_url}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False