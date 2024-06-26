from typing import List
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enqueue_mail(subject, message, emails: List[str]):
    send_mail(
        subject,
        message,
        from_email=None,
        recipient_list=emails,
        fail_silently=False,
    )
