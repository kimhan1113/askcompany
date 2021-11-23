from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

# min_length_validator = MinLengthValidator()
# min_length_validator("hello")
from django.shortcuts import resolve_url
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(validators=[MinLengthValidator(5)])
    # upload_to 는 미디어파일저장되는 경로를바꾼다 media다 저장되면 찾기 힘듬으로...
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y%m%d')
    tag_set = models.ManyToManyField('Tag', blank=True)
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Detail뷰가 구현이 되었다면 무조건 모델클래스에 get_absolute_url메소드를 구현하자!!!!!!!!!!

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        # return reverse('instagram:post_detail', args=[self.pk])
        return resolve_url('instagram:post_detail', self.pk)

    class Meta:
        ordering = ['-updated_at']

    def message_length(self):
        return len(self.message)



    # message_length 메소드에 이름부여
    message_length.short_description = "메세지 글자수"

class Comment(models.Model):

    # 위에 둘다 어느것이든지 동일한 결과임!
    # post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE)
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)

    # limit_choices_to 를 true로 하면 is_public에서 true인값만 나옴!
    post = models.ForeignKey(Post, on_delete=models.CASCADE, limit_choices_to=True) # post_id 필드가 생성된다.
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name