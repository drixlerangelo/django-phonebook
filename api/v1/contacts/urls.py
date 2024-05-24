from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AreaCodeListView, ContactViewSet

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
