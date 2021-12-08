from datetime import datetime, timedelta
from urllib.parse import quote


import pandas as pd
from io import StringIO

from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, \
    DeleteView

from instagram.decorator import post_ownership_required, post_delete_ownership_required
from instagram.forms import PostForm, NotClearableFileInput
from instagram.models import Post, PostImage


# post_list = login_required(ListView.as_view(model=Post, paginate_by=1))

# @method_decorator(login_required, name='dispatch')

# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if post.author != request.user:
#         messages.error(request, '작성자만 삭제할 수 있습니다.')
#         return redirect(post)
#
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스팅을 삭제했습니다.')
#         return redirect('instagram:post_list')
#     return render(request, 'instagram/post_confirm_delete.html',{
#         'post': post,
#     })

@method_decorator(post_delete_ownership_required, 'get')
@method_decorator(post_delete_ownership_required, 'post')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # success_url = reverse_lazy('instagram:post_list')

    def get_success_url(self):
        return reverse('instagram:post_list')


post_delete = PostDeleteView.as_view()


# @method_decorator(post_ownership_required, 'get')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10



    def get_queryset(self):
        #created_at__gte = timezone.now() - datetime.timedelta(days=1)
        # qs = super().get_queryset().filter(author=self.request.user, created_at__gte = timezone.now() - timedelta(days=1))

        qs = super().get_queryset().filter(author=self.request.user)

        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(message__icontains=q)
        return qs

post_list = PostListView.as_view()

@login_required
def post_new(request):

    if request.method == "POST":
        # post = Post()
        form = PostForm(request.POST, request.FILES)

        if form.is_valid(): # 유효성 검사가 수행됨!
            post = form.save(commit=False)

            post.author = request.user
            post.save()

            if(len(request.FILES.getlist('images')) > 10):
                messages.error(request, "이미지는 10개 이하로만 업로드가 가능합니다.")
                return redirect(reverse('instagram:post_new'))

            # get_absolute_url이 model에 적용 되어 있어야지만 아래 redirect가 반응한다.
            for img in request.FILES.getlist('images'):
                # Photo 객체를 하나 생성한다.
                photo = PostImage()
                # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                photo.post = post
                # pictures로부터 가져온 이미지 파일들을 저장한다.
                photo.image = img
                # 데이터베이스에 저장
                photo.save()

            messages.success(request, '포스팅을 저장했습니다.')
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html',{
        'form': form,
        'post': None,
    })

# @method_decorator(login_required, 'get')
# @method_decorator(login_required, 'post')
# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#
#     # def post(self, request, *args, **kwargs):
#     #     files = request.FILES.getlist('imgs')
#     #     for img in files:
#     #         photo = PostImage()
#     #         photo.post = Post
#     #         photo.img = img
#     #         photo.save(())
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.author = self.request.user
#         messages.success(self.request, '포스팅을 저장했습니다')
#         return super().form_valid(form)
#
#
# post_new = PostCreateView.as_view()



# updateview class를 함수형 뷰로 구현한것
@login_required
def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, '작성자만 수정할 수 있습니다.')
        return redirect(post)

    ImgFormSet = inlineformset_factory(Post, PostImage, fields=('image', ), can_delete=True, extra=10, max_num=10, widgets={'image': NotClearableFileInput})
    if request.method == "POST":
        form = ImgFormSet(request.POST, request.FILES, instance=post)
        # form_img = ImageForm(request.POST, request.FILES, instance=post_img)

        if form.is_valid():
            messages.success(request, '포스팅을 수정했습니다.')
            form.save()

            # post = form.save(commit=False)

            # post.author = request.user
            # request.user -> 현재 로그인 유저 instance
            # post.save()
            # get_absolute_url이 model에 적용 되어 있어야지만 아래 redirect가 반응한다.
            return redirect(post)
    else:
        form = ImgFormSet(instance=post)

    return render(request, 'instagram/post_formset.html', {
        'formset': form,
        'post': post,
    })


@method_decorator(post_ownership_required, 'get')
@method_decorator(post_ownership_required, 'post')
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_queryset(self):
        # 로그인이 되어있지 않으면 공개된것만 봐라!
        # qs = super().get_queryset()
        qs = super().get_queryset().filter(author=self.request.user)
        # if not self.request == :
        #     qs = qs.filter(is_public=True)
        return qs


    def form_valid(self, form):
        # post = form.save()
        # for img in self.request.FILES.getlist('imgs'):
        #     # Photo 객체를 하나 생성한다.
        #     photo = PostImage()
        #     # 외래키로 현재 생성한 Post의 기본키를 참조한다.
        #     photo.post = post
        #     # imgs로부터 가져온 이미지 파일 하나를 저장한다.
        #     photo.image = img
        #     # 데이터베이스에 저장
        #     photo.save()
        messages.success(self.request, '포스팅을 수정했습니다.')
        return super().form_valid(form)


# post_edit = PostUpdateView.as_view()

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

# @method_decorator(post_ownership_required, 'get')
class PostDetailView(DetailView):
    model = Post
    yesterday = datetime.today() - timedelta(seconds=86400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["yesterday"] = self.yesterday
        return context

    def get_queryset(self):

        # qs = super().get_queryset().filter(author=self.request.user, created_at__gte=timezone.now() - timedelta(days=1))
        qs = super().get_queryset().filter(author=self.request.user)
        # if not self.request == :
        #     qs = qs.filter(is_public=True)
        return qs


post_detail = PostDetailView.as_view()

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=1)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)

@login_required
def response_csv(request):
    df = pd.DataFrame([
        [100, 110, 120],
        [200, 210, 220],
        [300, 310, 320],
    ])
    encoded_filename = quote('pandas.csv')
    io = StringIO()
    df.to_csv(io)
    io.seek(0) # 끝에 있는 file cursor를 처음으로 이동
    response = HttpResponse(io, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(encoded_filename)
    return response


# def archives_year(request, year):
#
#     return HttpResponse(f'{year}년 archives')
