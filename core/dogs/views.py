from django.shortcuts import render
from django_filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from dogs.models import Dog, Breed
from dogs.permission import IsModer, IsOwner
from dogs.serializers import DogSerializer, BreedSerializer, DogDetailSerializer, BreedDetailSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

# Для пользователей - владельцев создайте пермишн IsOwner() ,
# который будет проверять является ли авторизованный пользователь владельцем продукта.
# Ограничьте доступ к собакам - пользователи могут видеть только своих собак в списке и просмотре одной собаке.
# Редактировать и удалять можно также только своих собак. Такие же права реализуйте для пород


class DogViewSet(ModelViewSet):
    # serializer_class = DogSerializer
    queryset = Dog.objects.all()
    permission_classes = [IsAuthenticated]

    default_serializers = DogSerializer
    stack_serializers = {
        'retrieve': DogDetailSerializer,
        'list': DogSerializer,
    }

    def get_serializer_class(self):
        return self.stack_serializers.get(self.action, self.default_serializers)

    def perform_create(self, serializer):
        new_dog = serializer.save()
        new_dog.owner = self.request.user
        new_dog.save()

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        return super().get_permissions()

    #
    # def list(self, request, *args, **kwargs):
    #     filter_backends = [SearchFilter, OrderingFilter]
    #     search_fields = ['breed']
    #     ordering_fields = ['date_born']
    #     return super().list(request, *args, **kwargs)


class BreedDetailView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class BreedListView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated]


class BreedCreateView(CreateAPIView):
    # queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, ~IsModer]


class BreedUpdateView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class BreedDeleteView(DestroyAPIView):
    # queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, IsOwner]
