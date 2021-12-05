import re

from django.forms import ModelForm

from instagram.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'message', 'photo', 'car_number', 'fran_name', 'as_1', 'as_2', 'as_3'
        ]


        # exclude는 비추 새로운 필드가 추가되었을 경우 바로 노출되기 때문에....
        # exclude = []

    # 영어는 저장안됨!
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            message = re.sub(r'[a-zA-Z]+', '', message)
        return message

