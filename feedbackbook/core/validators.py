import re

from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status


def year_validator(value):
    """Валидатор года."""
    if value > timezone.now().year:
        raise ValidationError("Год выпуска не может быть больше текущего!")


def username_validator(value):
    """Валидатор имени пользователя."""
    if value.lower() == 'me':
        raise ValidationError(
            f'Имя пользователя {value} недопустимо'
        )
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            "Имя может содержать только буквы, "
            "цифры и символы: '-', '_'"
        )


class CustomValidation(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Пользователь не найден'

    def __init__(self, detail, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
