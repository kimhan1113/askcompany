from datetime import datetime, timedelta

from django import template
from django.utils import timezone
from datetime import datetime, timedelta

from django.utils.timesince import timesince

from instagram.models import Post

register = template.Library()

@register.filter
def time_until(value):
    qs = Post.objects.filter(created_at__gte=timezone.now() - timedelta(days=1))
    now = datetime.now()
    print(now)
    try:
        difference = value - now
    except:
        print('에러!')
        return value

    if difference <= timedelta(days=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}