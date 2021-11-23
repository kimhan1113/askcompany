from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from instagram.models import Post


def post_ownership_required(func):

    def decorated(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if not post.author == request.user:
            messages.warning(request, '작성자만 수정할 수 있습니다.')
            return redirect(post)
        return func(request, *args, **kwargs)
    return decorated

def post_delete_ownership_required(func):

    def decorated(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if not post.author == request.user:
            messages.error(request, '작성자만 삭제할 수 있습니다.')
            return redirect(post)
        return func(request, *args, **kwargs)
    return decorated