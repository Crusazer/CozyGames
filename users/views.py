from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import generic

from users.forms import CreateUserForm, LoginUserForm, UserForm, ProfileForm
from users.models import Profile


# Create your views here.
class RegisterUser(CreateView):
    form_class = CreateUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        next_url = self.request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
        return response


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user:profile')
