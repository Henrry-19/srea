# Generated by Django 4.1.4 on 2023-04-03 18:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_rename_answer_question_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='due',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha'),
        ),
    ]
