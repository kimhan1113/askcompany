from django.conf import settings
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView

# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')
from accounts.forms import ProfileForm, PasswordChangingForm
from accounts.models import Profile

User = get_user_model()

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('accounts:profile')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

profile = ProfileView.as_view()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm

# profile_edit = ProfileUpdateView.as_view()

@login_required
def profile_edit(request):
    try:
        profile = request.user.profile

    except Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect(reverse('accounts:profile'))
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_form.html', {
        'form': form,
    })

class SignupView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('instagram:post_list')
    template_name = 'accounts/signup_form.html'

    def form_valid(self, form):

        if self.request.method == "POST":
            form = ProfileForm(self.request.POST, instance=get_user_model())
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = self.request.user
                profile.save()


signup = SignupView.as_view()

# signup = CreateView.as_view(
#     model=User,
#     form_class=UserCreationForm,
#     success_url=reverse_lazy('instagram:post_list'),
#     template_name='accounts/signup_form.html'
# )



# def signup(request):
#     pass

# def logout(request):
#     pass