from rest_framework import generics, permissions, viewsets
from .models import AreaCode, Contact
from .serializers import AreaCodeSerializer, ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('name')
    serializer_class = ContactSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user)

    def perform_create(self, serializer: ContactSerializer):
        serializer.save(account=self.request.user)

class AreaCodeListView(generics.ListAPIView):
    queryset = AreaCode.objects.all()
    serializer_class = AreaCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

