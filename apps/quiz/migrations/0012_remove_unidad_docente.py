# Generated by Django 4.1.4 on 2023-04-11 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_remove_quizzes_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unidad',
            name='docente',
        ),
    ]
