from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_number(value):
    value = str(value)

    if value.isdigit():
        return

    raise ValidationError(
        _(f'"{value}" is not a valid number'),
        params={"value": value},
    )