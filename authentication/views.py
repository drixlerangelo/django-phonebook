from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import AccountCreationForm
from allauth.mfa.models import Authenticator

def index(request: HttpRequest):
    if request.user.is_authenticated:
        authenticators = Authenticator.objects.filter(user=request.user)
        if not authenticators:
            return redirect('mfa_activate_totp')
        else:
            return render(request, 'home_index.html')
    return redirect('account_login')
