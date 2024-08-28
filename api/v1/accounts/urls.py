from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='accounts.index'),

    path(
        'api/v1/accounts/me/',
        views.AccountRetrieveView.as_view(),
        name='accounts-retrieve'
    ),
]
