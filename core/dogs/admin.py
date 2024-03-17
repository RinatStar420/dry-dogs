from django.contrib import admin

# Register your models here.
from dogs.models import Dog


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass