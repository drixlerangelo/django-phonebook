from rest_framework import serializers
from .models import AreaCode, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['uuid', 'name', 'area_code', 'number', 'email', 'address', 'url']
        read_only_fields = ['id', 'uuid']

    url = serializers.HyperlinkedIdentityField(
        view_name='contact-detail',
        lookup_field='uuid'
    )

class AreaCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaCode
        fields = ['id', 'code', 'telecom']
        read_only_fields = ['id']

    telecom = serializers.SerializerMethodField()

    def get_telecom(self, obj):
        return str(obj.telecom.name)
