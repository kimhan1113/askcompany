from django.urls import path

from blog1.views import post_list

urlpatterns = [
    path('', post_list, name='post_list'),
]