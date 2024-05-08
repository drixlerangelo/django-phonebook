from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class LoginInterfaceView(LoginView):
    template_name = 'login.html'

class LogoutInterfaceView(LogoutView):
    template_name = 'logout.html'

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = '/diaries'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('diary.list')
        return super().get(request, *args, **kwargs)

class Homeview(LoginRequiredMixin, TemplateView):
    template_name = 'home_index.html'
    extra_context = {
        'today': datetime.today()
    }
    login_url = '/login'

# class AuthorizedView(LoginRequiredMixin, TemplateView):
#     template_name = 'login.index'
#     login_url = '/admin'

def index(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, 'home_index.html')

    return redirect('login.index')
