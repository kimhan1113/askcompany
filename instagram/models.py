from datetime import timedelta, datetime

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
import pytz

# Create your models here.

# min_length_validator = MinLengthValidator()
# min_length_validator("hello")
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(validators=[MinLengthValidator(5)])
    # upload_to 는 미디어파일저장되는 경로를바꾼다 media다 저장되면 찾기 힘듬으로...


    # 차량번호
    car_number = models.CharField(max_length=13, blank=True)
    # 운수사명
    fran_name = models.CharField(max_length=10, blank=True)

    # A/S 리스트 Boolean
    as_1 = models.BooleanField(default=False, verbose_name='A/S 목록 1')
    as_2 = models.BooleanField(default=False, verbose_name='A/S 목록 2')
    as_3 = models.BooleanField(default=False, verbose_name='A/S 목록 3')

    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y%m%d')

    tag_set = models.ManyToManyField('Tag', blank=True)
    is_public = models.BooleanField(default=False, verbose_name='공개여부', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Detail뷰가 구현이 되었다면 무조건 모델클래스에 get_absolute_url메소드를 구현하자!!!!!!!!!!

    @property
    def sum_as(self):
        count = 0
        if self.as_1:
            count += 1
        if self.as_2:
            count += 1
        if self.as_3:
            count += 1

        return count

    # - timedelta(seconds=86400)

    def created_yesterday(self):
        return self.created_at - timedelta(seconds=86400)

    @property
    def check_oneday(self):
        local_tz = pytz.timezone('Asia/Seoul')
        utc = pytz.UTC

        # created_at = self.created_at.replace(tzinfo=pytz.utc).astimezone(local_tz).timestamp()
        created_at = self.created_at.replace(tzinfo=pytz.utc).astimezone(local_tz)

        # yesterday = (datetime.today() - timedelta(days=1.2)).replace(tzinfo=pytz.utc).timestamp()
        yesterday = (timezone.now() - timedelta(days=1)).replace(tzinfo=pytz.utc).astimezone(local_tz)

        # print(yesterday)
        # print(created_at)

        # created_at_date = self.created_at.replace(tzinfo=pytz.utc).astimezone(local_tz)
        # yesterday_date = (datetime.today() - timedelta(days=1.5)).replace(tzinfo=pytz.utc)

        # print(created_yesterday.replace(tzinfo=pytz.utc).astimezone(local_tz))
        # print(created_yesterday.replace(tzinfo=None))
        # print(yesterday.replace(tzinfo=None))

        # print(created_at_date)
        # print(yesterday_date)

        # print(created_at)
        # print(yesterday)

        if(created_at > yesterday):
            return True
        else:
            return False

        # return self.created_at - timedelta(seconds=86400)

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # post_id 필드가 생성된다.
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if(self.message):
            return self.message

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='instagram/post/%Y%m%d', blank=True, null=True)

    # def __str__(self):
    #     return self.post.message