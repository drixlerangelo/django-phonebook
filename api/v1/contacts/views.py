from rest_framework import generics, permissions
from .models import AreaCode, Contact
from .serializers import AreaCodeSerializer, ContactSerializer

class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all().order_by('name')
    serializer_class = ContactSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user)

    def perform_create(self, serializer: ContactSerializer):
        serializer.save(account=self.request.user)

class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAuthenticated]

class AreaCodeListView(generics.ListAPIView):
    queryset = AreaCode.objects.all()
    serializer_class = AreaCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

