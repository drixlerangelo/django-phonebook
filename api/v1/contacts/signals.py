from actstream import action
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from core.mixins import AppBroadcaster

@receiver([post_delete, post_save])
def notify_owner(sender, instance, created: bool | None = None, *args, **kwargs):
    broadcaster = AppBroadcaster()

    # Avoids circular import errors
    from api.v1.contacts.models import Contact
    if sender == Contact:
        if created is None:
            subject = 'Contact Deleted'
            message = 'A contact has been deleted.'
            broadcaster.notify(
                'contact-deletion',
                {'uuid': str(instance.uuid)},
                instance.account,
            )
            action.send(
                instance.account,
                verb='deleted',
                action_object=instance
            )
        elif created:
            subject = 'New Contact Created'
            message = 'A new contact has been created.'
            broadcaster.notify(
                'contact-creation',
                {'uuid': str(instance.uuid)},
                instance.account,
            )
            action.send(
                instance.account,
                verb='created',
                action_object=instance
            )
        else:
            subject = 'Contact Updated'
            message = 'A contact has been updated.'
            broadcaster.notify(
                'contact-modification',
                {'uuid': str(instance.uuid)},
                instance.account,
            )
            action.send(
                instance.account,
                verb='updated',
                action_object=instance
            )
        send_mail(
            subject,
            message,
            from_email=None,
            recipient_list=[instance.account.email],
            fail_silently=False,
        )
