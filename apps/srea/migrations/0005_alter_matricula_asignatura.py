# Generated by Django 4.1.4 on 2023-01-23 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('srea', '0004_alter_pregunta_test_alter_respuesta_pregunta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matricula',
            name='asignatura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignatura', to='srea.asignatura'),
        ),
    ]
