# Generated by Django 4.2.1 on 2023-06-20 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_rename_user_indicacion_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicacion',
            name='autor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
    ]
