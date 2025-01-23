from django.core.exceptions import ValidationError
from django.utils.timezone import now

def validate_year(value):
    current_year = now().year
    if value > current_year:
        raise ValidationError(f'Год издания не может быть больше {current_year}.')
    if value < 0:  # если хотите исключить слишком старые года
        raise ValidationError('Год издания не может быть отрицательным.')

