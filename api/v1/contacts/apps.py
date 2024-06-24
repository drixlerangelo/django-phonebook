from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.contacts'

    def ready(self):
        from actstream import registry
        from api.v1.contacts import signals
        registry.register(self.get_model('Contact'))
