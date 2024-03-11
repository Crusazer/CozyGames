from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreateUserForm, LoginUserForm


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

