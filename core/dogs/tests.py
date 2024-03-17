from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from dogs.models import Dog, Breed
from users.models import User


class DogTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test1@test1.com', is_superuser=True
        )

        self.breed = Breed.objects.create(
            name='Test',
            description='Test'
        )

        self.dog = Dog.objects.create(
            name='Test',
            breed=self.breed,
            owner=self.user
        )

        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        self.user = User.objects.create(email='test@test.com', is_superuser=True)
        self.user.groups.add(moderator_group)

    def test_get_list(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/dogs/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
