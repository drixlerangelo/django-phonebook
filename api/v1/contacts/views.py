from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, authentication, filters

from api.v1.accounts.models import Account
from app import settings
from .models import AreaCode, Contact
from .serializers import AreaCodeSerializer, ContactSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .mixins import ContactsPagination
from django.core.mail import send_mail

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('name')
    serializer_class = ContactSerializer
    lookup_field = 'uuid'
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'name', 'number']
    search_fields = ['id', 'name', 'number', 'area_code__code']
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ContactsPagination

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user)

    def perform_create(self, serializer: ContactSerializer):
        account: Account = self.request.user
        serializer.save(account=account)

        send_mail(
            'New Contact Created',
            'A new contact has been created.',
            from_email=None,
            recipient_list=[account.email],
            fail_silently=False,
        )

    def perform_update(self, serializer):
        account: Account = self.request.user
        serializer.save(account=account)

        send_mail(
            'Contact Updated',
            'A contact has been updated.',
            from_email=None,
            recipient_list=[account.email],
            fail_silently=False,
        )

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

class AreaCodeListView(generics.ListAPIView):
    queryset = AreaCode.objects.all()
    serializer_class = AreaCodeSerializer
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
