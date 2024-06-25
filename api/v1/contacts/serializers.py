from actstream.models import Action
from rest_framework import serializers
from .models import AreaCode, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'uuid', 'name', 'area_code', 'number', 'email', 'address', 'url']
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

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['verb', 'actor', 'action_object', 'timestamp', '__str__']

    actor = serializers.SerializerMethodField()
    action_object = serializers.SerializerMethodField()

    def get_actor(self, obj):
        return obj.actor.username

    def get_action_object(self, obj):
        return f"{obj.action_object_content_type}:{obj.action_object.uuid}"
