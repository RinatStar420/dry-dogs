from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from dogs.models import Dog
from users.models import User


@shared_task
def send_message_like(user_id, dog_id):
    user = User.objects.get(pk=user_id)
    dog = Dog.objects.get(pk=dog_id)
    send_mail(subject=f'лайк для собаки {dog}',
              message=f'Вы поставили лайк собаке {dog}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[f'{user.email}',])

    # subject,
    # message,
    # from_email,
    # recipient_list,