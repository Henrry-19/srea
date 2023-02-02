# Generated by Django 4.1.4 on 2023-02-02 16:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('srea', '0008_alter_carrera_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignatura',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
