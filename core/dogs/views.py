from django.shortcuts import render
from django_filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dogs.models import Dog, Breed
from dogs.paginators import CustomPagination
from dogs.permission import IsModer, IsOwner
from dogs.serializers import DogSerializer, BreedSerializer, DogDetailSerializer, BreedDetailSerializer, \
    DonationSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404

# Для пользователей - владельцев создайте пермишн IsOwner() ,
# который будет проверять является ли авторизованный пользователь владельцем продукта.
# Ограничьте доступ к собакам - пользователи могут видеть только своих собак в списке и просмотре одной собаке.
# Редактировать и удалять можно также только своих собак. Такие же права реализуйте для пород
from dogs.services import get_link
from dogs.tasks import send_message_like
from users.models import User


class DogViewSet(ModelViewSet):
    # serializer_class = DogSerializer
    queryset = Dog.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

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
    pagination_class = CustomPagination


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


class DonationCreateApiView(CreateAPIView):
    serializer_class = DonationSerializer

    def perform_create(self, serializer):
        new_donation = serializer.save()
        payment_link, session_id = get_link(new_donation.donation_amount)
        new_donation.payment_link = payment_link
        new_donation.payment_id = session_id
        new_donation.save()


class SetLikeToDog(APIView):

    def post(self, request):
        user = get_object_or_404(User, pk=request.data.get('user'))
        dog = get_object_or_404(Dog, pk=request.data.get('dog'))
        if dog.likes.filter(id=user.id).exists():
            return Response({"result": f"Лайк для собаки {dog} УЖЕ добавлен от {user}"}, status=200)
        dog.likes.add(user)
        send_message_like.delay(user.id, dog.id)
        return Response({"result": f"Лайк для собаки {dog} добавлен от {user}"}, status=200)
