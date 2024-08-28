from django.shortcuts import redirect
from django.http import HttpRequest
from app import settings
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import authentication, generics, permissions, throttling
from .models import Account
from .serializers import AccountSerializer

def index(request: HttpRequest):
    if request.user.is_authenticated:
        if settings.MFA_ENABLED == True:
            from allauth.mfa.models import Authenticator
            authenticators = Authenticator.objects.filter(user=request.user)
            if not authenticators:
                return redirect('mfa_activate_totp')
        return redirect('swagger-ui')
    return redirect('account_login')

class AccountRetrieveView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle, throttling.AnonRateThrottle]
    lookup_field = 'username'

    def get_object(self):
        return self.queryset.get(username=self.request.user.username)
