from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UsersForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': '帳號',
            'email': '信箱',
            'password1': '密碼',
            'password2': '確認密碼'
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages['unique'] = "該帳號已存在。"
        self.fields['email'].error_messages = {'unique': '此電子郵件地址已被使用。'}
        self.fields['password2'].error_messages = {'password_mismatch': "兩次輸入的密碼不一致"}
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise ValidationError("帳號需要4個字")
        if len(username) > 10:
            raise ValidationError("帳號不能超過10個字")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("該信箱已被註冊")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if len(password1) < 4:
                raise ValidationError("密碼需要至少4個字")
            if len(password1) > 10:
                raise ValidationError("密碼不能超過10個字")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "兩次輸入的密碼不一致")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='信箱', required=True)
