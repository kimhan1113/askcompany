from django.urls import path

from blog1.views import post_list

app_name = 'blog1' # URL Reverse namespace 역할 하게 됨

urlpatterns = [
    path('', post_list, name='post_list'),
]