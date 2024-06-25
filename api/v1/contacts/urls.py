from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import settings
from .views import AreaCodeListView, ActivityListView, ContactViewSet, test

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path(
        'area-codes/',
        AreaCodeListView.as_view(),
        name='area-code-list'
    ),

    path(
        'activities/',
        ActivityListView.as_view(),
        name='activity-list'
    ),
]

if settings.DEBUG == True:
    urlpatterns += [
        path('test/', test),
    ]
