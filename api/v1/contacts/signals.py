from django.apps import AppConfig
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save)
def send_email(sender, instance, created: bool, *args, **kwargs):
    from api.v1.contacts.models import Contact
    if sender == Contact:
        if created:
            send_mail(
                'New Contact Created',
                'A new contact has been created.',
                from_email=None,
                recipient_list=[instance.account.email],
                fail_silently=False,
            )
        else:
            send_mail(
                'Contact Updated',
                'A contact has been updated.',
                from_email=None,
                recipient_list=[instance.account.email],
                fail_silently=False,
            )

class ContactConfig(AppConfig):
    name = 'api.v1.contacts.signals'
    verbose_name = 'Contact Config'

    def ready(self):
        from api.v1.contacts import signals
