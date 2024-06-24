from django.apps import AppConfig



class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.accounts'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Account'))
