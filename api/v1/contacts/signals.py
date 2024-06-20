from django.apps import AppConfig
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver([post_delete, post_save])
def notify_owner(sender, instance, created: bool = None, *args, **kwargs):
    from api.v1.contacts.models import Contact
    if sender == Contact:
        if created is None:
            subject = 'Contact Deleted'
            message = 'A contact has been deleted.'
        elif created:
            subject = 'New Contact Created'
            message = 'A new contact has been created.'
        else:
            subject = 'Contact Updated'
            message = 'A contact has been updated.'
        send_mail(
            subject,
            message,
            from_email=None,
            recipient_list=[instance.account.email],
            fail_silently=False,
        )

class ContactConfig(AppConfig):
    name = 'api.v1.contacts.signals'
    verbose_name = 'Contact Config'

    def ready(self):
        from api.v1.contacts import signals
