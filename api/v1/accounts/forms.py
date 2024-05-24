from django import forms
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import SignupForm

from .models import Account


class AccountCreationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(required=True)
        self.fields['last_name'] = forms.CharField(required=True)
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email']


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ['username']
