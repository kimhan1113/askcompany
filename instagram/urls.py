from django.urls import path, re_path, register_converter

from instagram.converters import YearConverter, MonthConverter, DayConverter
from instagram.views import post_list, post_detail, post_archive, post_archive_year, post_new, post_edit, post_delete

# from instagram.views import archives_year

app_name = 'instagram' # URL Reverse namespace 역할 하게 됨


register_converter(YearConverter, 'year')
register_converter(MonthConverter, 'month')
register_converter(DayConverter, 'day')

# Post.objects.all().values_list('create_at')
# Post.objects.all().values_list('create_at__year')
# Post.objects.all().values_list('create_at__year', flat=True)

urlpatterns = [
    path('new/', post_new, name='post_new'),
    path('<int:pk>/edit/', post_edit, name='post_edit'),
    path('<int:pk>/delete/', post_delete, name='post_delete'),

    path('', post_list, name='post_list'),
    path('<int:pk>', post_detail, name='post_detail'),

    # re_path(r'archives/(?P<year>\d+)/', archives_year),

    # 숫자 4개만 입력받음
    # re_path(r'archives/(?P<year>\d{4})/', archives_year),

    # 20으로 시작하는 숫자 4개만 입력받음
    # re_path(r'archives/(?P<year>20\d{2})/', archives_year),

    path('archive/', post_archive, name='post_archive'),
    path('archive/<year:year>/', post_archive_year, name='post_archive_year'),
    # path('archive/<year:year>/<month:month>/', post_archive_month, name='post_archive_month'),
    # path('archive/<year:year>/<month:month>/<day:Day>', post_archive_day, name='post_archive_day'),

    # 첫번째 year는 converter이름이고 두번째 year는 전달할 인자
    # path('archives/<year:year>/', archives_year),



]