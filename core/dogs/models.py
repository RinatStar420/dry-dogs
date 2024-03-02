from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name="Кличка")
    breed = models.ForeignKey("dogs.Breed", verbose_name="Порода собаки", related_name="dogs",
                              on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to="dog_photo", verbose_name="Картинка", null=True, blank=True)
    date_born = models.DateField(verbose_name="Дата рождения", null=True)

    owner = models. ForeignKey("users.User", on_delete=models.CASCADE, )

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"
        ordering = ['breed', 'name', ]

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"
        ordering = ['name', ]

    def __str__(self):
        return self.name