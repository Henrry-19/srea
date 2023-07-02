# Generated by Django 4.2.1 on 2023-06-24 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('srea', '0009_remove_asignatura_docente'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUploaded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='archivo/%Y/%m/%d')),
                ('observation', models.CharField(max_length=200, null=True, verbose_name='Observation')),
                ('unid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seleccionar_unidad', to='srea.unidad', verbose_name='Seleccionar unidad')),
            ],
            options={
                'verbose_name': 'file_uploaded',
                'verbose_name_plural': 'file_uploadeds',
                'db_table': 'file_uploaded',
                'ordering': ['id'],
            },
        ),
    ]
