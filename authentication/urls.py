from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mfa_check.index'),
]
