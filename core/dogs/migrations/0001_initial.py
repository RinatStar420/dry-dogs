# Generated by Django 4.2 on 2024-02-17 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Порода',
                'verbose_name_plural': 'Породы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Кличка')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='dog_photo', verbose_name='Картинка')),
                ('date_born', models.DateField(null=True, verbose_name='Дата рождения')),
                ('breed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dogs', to='dogs.breed', verbose_name='Порода собаки')),
            ],
            options={
                'verbose_name': 'Собака',
                'verbose_name_plural': 'Собаки',
                'ordering': ['breed', 'name'],
            },
        ),
    ]
