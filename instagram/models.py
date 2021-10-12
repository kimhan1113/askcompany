from django.db import models

# Create your models here.

class Post(models.Model):
    message = models.TextField()
    # upload_to 는 미디어파일저장되는 경로를바꾼다 media다 저장되면 찾기 힘듬으로...
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y%m%d')
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    def message_length(self):
        return len(self.message)

    # message_length 메소드에 이름부여
    message_length.short_description = "메세지 글자수"