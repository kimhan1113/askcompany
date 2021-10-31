from django.urls import path, re_path, register_converter

from instagram.views import post_list, post_detail, archives_year

app_name = 'instagram' # URL Reverse namespace 역할 하게 됨

class YearConverter:
    regex = r"20\d{2}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value

register_converter(YearConverter, "year")

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:pk>', post_detail),
    # re_path(r'archives/(?P<year>\d+)/', archives_year),

    # 숫자 4개만 입력받음
    # re_path(r'archives/(?P<year>\d{4})/', archives_year),

    # 20으로 시작하는 숫자 4개만 입력받음
    re_path(r'archives/(?P<year>20\d{2})/', archives_year),

    # 첫번째 year는 converter이름이고 두번째 year는 전달할 인자
    path('archives/<year:year>/', archives_year),



]