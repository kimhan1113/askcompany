import random
import time

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Profile

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