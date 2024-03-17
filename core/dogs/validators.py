from rest_framework.exceptions import ValidationError

scam_words = ['ставки', 'крипта', 'продам', 'гараж']


def validators_scam_words(value):
    if value.lower() in scam_words:
        raise ValidationError("Использованы запрещенные символы")
