# Generated by Django 4.1.4 on 2023-03-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_unidad_docente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unidad',
            name='nombre',
            field=models.CharField(max_length=150, verbose_name='Nombre'),
        ),
    ]
