from rest_framework import serializers

from dogs.models import Dog, Breed, Donation
from rest_framework.fields import SerializerMethodField

from dogs.validators import validators_scam_words


class DogSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validators_scam_words])
    class Meta:
        model = Dog
        fields = "__all__"


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = "__all__"


class BreedDetailSerializer(serializers.ModelSerializer):
    dog_this_breed = SerializerMethodField()

    def get_dog_this_breed(self, breed):
        return [dog.name for dog in Dog.objects.filter(breed=breed)]

    class Meta:
        model = Breed
        fields = "__all__"


class DogDetailSerializer(serializers.ModelSerializer):
    breed = BreedDetailSerializer()
    dog_with_same_breed = SerializerMethodField()

    def get_dog_with_same_breed(self, dog):
        return Dog.objects.filter(breed=dog.breed).count()

    class Meta:
        model = Dog
        fields = ('name', 'breed', 'dog_with_same_breed')


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'