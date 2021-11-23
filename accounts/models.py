from django.conf import settings
from django.db import models
from django.shortcuts import resolve_url


class Profile(models.Model):

    # foreignkey (unique=true) 와 유사하지만, reverse 차이!
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=6)

    # def get_absolute_url(self):
    #     # return reverse('instagram:post_detail', args=[self.pk])
    #     return resolve_url('accounts:profile', self.pk)