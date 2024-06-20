import uuid
from django.db import models
from django.core.validators import EmailValidator

from api.v1.accounts.models import Account
from api.v1.contacts.validations import validate_number
from core.models import SoftDeleteModel

class Telecom(models.Model):
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.name

class AreaCode(models.Model):
    # On delete options: https://sentry.io/answers/django-on-delete/
    telecom = models.ForeignKey(Telecom, on_delete=models.DO_NOTHING)
    # 63 - country code; 9xx - mobile; 2x - landline; 32-88x - landline
    # 639xx - mobile; 6345x - landline; 632x - landline
    # https://en.wikipedia.org/wiki/Telephone_numbers_in_the_Philippines#Mobile_phone_area_codes
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.code

class Contact(SoftDeleteModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)
    name = models.CharField(max_length=255, blank=False)
    area_code = models.ForeignKey(AreaCode, on_delete=models.DO_NOTHING, blank=False)
    number = models.CharField(
        max_length=8,
        blank=False,
        validators=[validate_number])
    email = models.EmailField(
        validators=[EmailValidator()],
        blank=False
    )
    address = models.TextField(blank=False)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
