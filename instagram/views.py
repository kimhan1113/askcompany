from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView

from instagram.forms import PostForm
from instagram.models import Post


# post_list = login_required(ListView.as_view(model=Post, paginate_by=1))

# @method_decorator(login_required, name='dispatch')

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 2

post_list = PostListView.as_view()

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid(): # 유효성 검사가 수행됨!
            post = form.save(commit=False)
            post.author = request.user
            post = form.save()
            messages.success(request, '포스팅을 저장했습니다.')
            # get_absolute_url이 model에 적용 되어 있어야지만 아래 redirect가 반응한다.
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html',{
        'form': form,
        'post': None,
    })


# updateview class를 함수형 뷰로 구현한것
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, '작성자만 수정할 수 있습니다.')
        return redirect(post)


    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, '포스팅을 수정했습니다.')
            # post.author = request.user
            # request.user -> 현재 로그인 유저 instance
            # post.save()
            # get_absolute_url이 model에 적용 되어 있어야지만 아래 redirect가 반응한다.
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(request, 'instagram/post_form.html',{
        'form': form,
        'post': post,
    })

# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     messages.info(request, 'messages 테스트')
#
#     # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html', {
#         'post_list': qs,
#         'q': q,
#     })

# 클래스 기반뷰에 뷰 앞에다가 아래와 같이 적용하여 로그인 여부를 확인 후 실행!
class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'



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
# post_detail = DetailView.as_view(
#     model=Post,
#     queryset=Post.objects.filter(is_public=True))

class PostDetailView(DetailView):
    model = Post

    # queryset = Post.objects.filter(is_public=True)

    # def get_queryset(self):
    #     # 로그인이 되어있지 않으면 공개된것만 봐라!
    #     qs = super().get_queryset()
    #     if not self.request.user.is_authenticated:
    #         qs = qs.filter(is_public=True)
    #     return qs

post_detail = PostDetailView.as_view()

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=1)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)


# def archives_year(request, year):
#
#     return HttpResponse(f'{year}년 archives')