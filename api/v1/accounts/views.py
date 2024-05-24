from django.shortcuts import render, redirect
from django.http import HttpRequest
from allauth.mfa.models import Authenticator

def index(request: HttpRequest):
    if request.user.is_authenticated:
        authenticators = Authenticator.objects.filter(user=request.user)
        if not authenticators:
            return redirect('mfa_activate_totp')
        else:
            return redirect('swagger-ui')
    return redirect('account_login')
