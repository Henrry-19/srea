# Generated by Django 4.1.4 on 2023-02-18 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('srea', '0014_respuesta_correcta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pregunta',
            old_name='pregunta',
            new_name='texto',
        ),
    ]
