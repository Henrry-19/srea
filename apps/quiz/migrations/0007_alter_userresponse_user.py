# Generated by Django 4.2.1 on 2023-07-01 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0006_delete_fileuploaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_response', to=settings.AUTH_USER_MODEL),
        ),
    ]
