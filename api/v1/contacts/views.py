from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, authentication, filters
from .models import AreaCode, Contact
from .serializers import AreaCodeSerializer, ContactSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .mixins import ContactsPagination

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
        serializer.save(account=self.request.user)

class AreaCodeListView(generics.ListAPIView):
    queryset = AreaCode.objects.all()
    serializer_class = AreaCodeSerializer
    authentication_classes = [OAuth2Authentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
