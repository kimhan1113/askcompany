from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from instagram.models import Post, Comment, Tag


# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author','photo_tag', 'message', 'message_length', 'is_public', 'created_at', 'updated_at']

    # 메세지에 링크가 잡힘
    list_display_links = ['message']

    # 날짜 필터걸어서 오른쪽에 필터생김
    list_filter = ['created_at', 'updated_at', 'is_public']

    # 찾는 필터 생성 (여러가지 추가해서 필터걸수있다 지금은 ok랑 메세지 걸어서 둘다 찾을수있다)
    search_fields = ['pk', 'message']
    # form = PostForm

    def photo_tag(self, post):
        if post.photo:
            return mark_safe(f'<img src="{post.photo.url}" style="width: 100px;" />')
        return None


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass




# admin.site.register(Post, PostAdmin)