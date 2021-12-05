import random
import time

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from accounts.models import Profile

User = get_user_model()

class LoginForm(AuthenticationForm):
    random.seed(int(time.time()))
    a = random.randrange(1, 10)
    b = random.randrange(1, 10)
    answer = forms.IntegerField(help_text=f'{a} + {b} = ?')

    ans = int(a) + int(b)
    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if answer != self.ans:
            raise forms.ValidationError('땡~!')


        return answer




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'zipcode']

# class PasswordChangeForm(forms.ModelForm):
#     pass

class PasswordChangingForm(PasswordChangeForm):

    old_password = forms.CharField(label="현재 비밀번호", widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': '현재 비밀번호'}))
    new_password1 = forms.CharField(label="새 비밀번호", widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': '새 비밀번호'}))
    new_password2 = forms.CharField(label="새 비밀번호 확인", widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': '새 비밀번호 확인'}))

    def clean_new_password1(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')

        if old_password and new_password1:
            if old_password == new_password1:
                raise ValidationError("새로운 암호는 기존 암호와 다르게 입력해주세요.")
        return new_password1

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

