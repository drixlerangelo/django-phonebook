from django.shortcuts import redirect
from django.http import HttpRequest
from app import settings

def index(request: HttpRequest):
    if request.user.is_authenticated:
        if settings.MFA_ENABLED == True:
            from allauth.mfa.models import Authenticator
            authenticators = Authenticator.objects.filter(user=request.user)
            if not authenticators:
                return redirect('mfa_activate_totp')
        return redirect('swagger-ui')
    return redirect('account_login')
