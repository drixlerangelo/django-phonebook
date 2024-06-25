"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import oauth2_provider.views as oauth2_views
from app import settings
from allauth.account import views

# App views
urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        # Admin page
        path('admin/', admin.site.urls),

        # Download the schema
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
    ]

urlpatterns += [
    # Index page
    path('', include('api.v1.accounts.urls')),

    # App homepage - Swagger
    path('swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),

    # Auth endpoints
    path('accounts/', include([
        path('login/', views.login, name='account_login'),
        path('logout/', views.logout, name='account_logout'),
        path('signup/', views.signup, name='account_signup'),
        path('reauthenticate/', views.reauthenticate, name='account_reauthenticate'),
        path('mfa/', include('allauth.mfa.urls')),
        path('email/', views.email, name='account_email'),
        path(
            'confirm-email/',
            views.email_verification_sent,
            name='account_email_verification_sent',
        ),
        re_path(
            r'^confirm-email/(?P<key>[-:\w]+)/$',
            views.confirm_email,
            name='account_confirm_email',
        ),
    ])),

    # OAuth 2 endpoints:
    # need to pass in a tuple of the endpoints as well as the app's name
    # because the app_name attribute is not set in the included module
    path('oauth/', include(
        ([
            path('authorize/', oauth2_views.AuthorizationView.as_view(), name='authorize'),
            path('token/', oauth2_views.TokenView.as_view(), name='token'),
            path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name='revoke-token'),
        ], 'oauth2_provider'),
        namespace='oauth2_provider'
    )),

    # API endpoints
    path('api/', include([
        path('v1/', include([
            path('', include('api.v1.contacts.urls')),
        ])),
    ])),
]
