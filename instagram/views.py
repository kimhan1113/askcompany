from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

from instagram.models import Post


post_list = ListView.as_view(model=Post)


# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html', {
#         'post_list': qs,
#         'q': q,
#     })


# def post_detail(request: HttpRequest, pk:int) -> HttpResponse:
#
#     post = get_object_or_404(Post, pk=pk)
#
#     # 위 코드가 아래 코드랑 동일 (페이지가 없는 pk에 대해서 not exist 에러를 띄움!
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except Post.DoesNotExist:
#     #     raise Http404
#
#     return render(request, 'instagram/post_detail.html', {
#         'post': post,
#     })


# 위 함수형 코드랑 동일함!!
post_detail = DetailView.as_view(model=Post)



def archives_year(request, year):

    return HttpResponse(f'{year}년 archives')