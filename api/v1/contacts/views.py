from actstream.models import actor_stream
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, authentication, filters, throttling

from api.v1.accounts.models import Account
from .models import AreaCode, Contact
from .serializers import AreaCodeSerializer, ContactSerializer, ActionSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from core.mixins import BasePagination
import pandas as pd

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('name')
    serializer_class = ContactSerializer
    lookup_field = 'uuid'
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'name', 'number']
    search_fields = ['id', 'name', 'number', 'area_code__code']
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasePagination
    throttle_classes = [throttling.UserRateThrottle, throttling.AnonRateThrottle]

    def get_queryset(self):
        return self.queryset.filter(
            account=self.request.user,
            is_deleted=False,
        )

    def perform_create(self, serializer: ContactSerializer):
        account: Account = self.request.user
        serializer.save(account=account)

    def perform_update(self, serializer):
        account: Account = self.request.user
        serializer.save(account=account)

    def list(self, request: HttpRequest, *args, **kwargs):
        if request.query_params.get('type') == 'export':
            queryset = self.filter_queryset(self.get_queryset())

            # Convert the queryset to a DataFrame
            if queryset.count() > 0:
                df = pd.DataFrame.from_records(queryset.values('name', 'area_code__code', 'number', 'email', 'address'))
            else:
                df = pd.DataFrame({
                    'name': [],
                    'area_code__code': [],
                    'number': [],
                    'email': [],
                    'address': [],
                })

            # Rename columns
            df.columns = ['Contact Name', 'Area Code', 'Phone Number', 'Email', 'Address']

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'
            df.to_excel(response, index=False)

            return response
        else:
            return super().list(request, *args, **kwargs)

class AreaCodeListView(generics.ListAPIView):
    queryset = AreaCode.objects.all()
    serializer_class = AreaCodeSerializer
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle, throttling.AnonRateThrottle]

class ActivityListView(generics.ListAPIView):
    serializer_class = ActionSerializer
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle, throttling.AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['timestamp']

    def get_queryset(self):
        # Get the stream of actions for the logged-in user
        queryset = actor_stream(self.request.user)

        # Get the contact's UUID from the query parameters
        search_uuid = self.request.query_params.get('search')

        if search_uuid:
            # Get the specific contact
            contact = get_object_or_404(Contact, uuid=search_uuid)

            # Filter the actions for this contact
            queryset = queryset.filter(action_object_object_id=contact.id)

        return queryset

@login_required
def test(request: HttpRequest) -> HttpResponse:
    """
    Test the Contacts' experimental functionalities.
    """
    return render(request, 'test.html')
