# Generated by Django 4.1.4 on 2023-01-31 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srea', '0007_remove_asignatura_user_alter_carrera_curso'),
        ('user', '0003_remove_user_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='curso',
            field=models.ManyToManyField(blank=True, related_name='ciclo', to='srea.curso', verbose_name='Ciclos'),
        ),
    ]
