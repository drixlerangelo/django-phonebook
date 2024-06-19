from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserChangeForm
from allauth.account.utils import send_email_confirmation
from .models import Account


class AccountCreationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(required=True)
        self.fields['last_name'] = forms.CharField(required=True)
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, request):
        user = super(AccountCreationForm, self).save(request)
        send_email_confirmation(request, user, True, user.email)
        return user


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ['username']
