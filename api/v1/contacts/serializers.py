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

    def validate(self, data):
        area_code = data.get('area_code')
        number = data.get('number')
        account = self.context['request'].user

        # Check if this is an update operation
        if self.instance:
            has_same_area_code = self.instance.area_code == area_code
            has_same_number = self.instance.number == number

            # If the area_code and number are not being changed, skip the duplicate check
            if has_same_area_code and has_same_number:
                return data

        # Check for duplicates only within the contacts of the currently logged-in user
        if Contact.objects.filter(account=account, area_code=area_code, number=number).exists():
            raise serializers.ValidationError({
                'area_code': 'A contact with this area code and number already exists.',
                'number': 'A contact with this area code and number already exists.',
            })

        return data

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
