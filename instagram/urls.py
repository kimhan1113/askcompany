from django.urls import path

from instagram.views import post_list

app_name = 'instagram'

urlpatterns = [
    path('', post_list, name='post_list'),
]