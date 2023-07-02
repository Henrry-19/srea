# Generated by Django 4.2.1 on 2023-06-19 15:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_users_indicacion_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicacion',
            name='user_indicacion',
            field=models.ManyToManyField(blank=True, related_name='user_ind', to=settings.AUTH_USER_MODEL, verbose_name='Indicación de usuarios'),
        ),
    ]
