# Generated by Django 4.2.1 on 2023-06-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_question_quiz'),
        ('srea', '0003_alter_catalogitem_catalog_remove_unidad_quizzes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unidad',
            name='quizzes',
        ),
        migrations.AddField(
            model_name='unidad',
            name='quizzes',
            field=models.ManyToManyField(related_name='quizzes', to='quiz.quiz', verbose_name='quizzes'),
        ),
    ]
