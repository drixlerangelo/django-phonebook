from django.http import HttpRequest, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, authentication, filters, throttling

from api.v1.accounts.models import Account
from .models import AreaCode, Contact
from .serializers import AreaCodeSerializer, ContactSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from core.mixins import BasePagination
from django.core.mail import send_mail
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

    def perform_destroy(self, instance: Contact):
        account: Account = self.request.user
        instance.delete()

        send_mail(
            'Contact Deleted',
            'A contact has been deleted.',
            from_email=None,
            recipient_list=[account.email],
            fail_silently=False,
        )

    def list(self, request: HttpRequest, *args, **kwargs):
        if request.query_params.get('type') == 'export':
            queryset = self.filter_queryset(self.get_queryset())

            # Convert the queryset to a DataFrame
            df = pd.DataFrame.from_records(queryset.values('name', 'area_code__code', 'number', 'email', 'address'))

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
