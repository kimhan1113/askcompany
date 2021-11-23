from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import LoginForm
from accounts.views import profile, profile_edit, signup

app_name = 'accounts'

# app_name을 넣으면 무조건 reserve('accounts:profile')이런식으로 url을 만들어야한다
# url 'profile'이렇게 쓰고 싶으면 app_name이 없고 name만 설정해야한다!

urlpatterns = [
    # 로그인 되어있는데 로그인페이지로 임의로 들어가면 redirect_authenticated_user =True로 해준다, 그리고 setting가서 설정!
    path('login/', LoginView.as_view(template_name='accounts/login_form.html', form_class=LoginForm, redirect_authenticated_user =True), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]