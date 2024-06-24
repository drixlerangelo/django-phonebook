from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import settings
from .views import AreaCodeListView, ContactViewSet, test

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path(
        'area-codes/',
        AreaCodeListView.as_view(),
        name='area-code-list'
    ),
]

if settings.DEBUG == True:
    urlpatterns += [
        path('test/', test),
    ]
