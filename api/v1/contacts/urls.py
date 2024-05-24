from django.urls import path
from .views import AreaCodeListView, ContactListCreateView, ContactRetrieveUpdateDestroyView

urlpatterns = [
    path(
        'contacts/',
        ContactListCreateView.as_view(),
        name='contact-list-create'
    ),
    path(
        'contacts/<uuid:uuid>/',
        ContactRetrieveUpdateDestroyView.as_view(),
        name='contact-retrieve-update-destroy'
    ),

    path(
        'area-codes/',
        AreaCodeListView.as_view(),
        name='area-code-list'
    ),
]
