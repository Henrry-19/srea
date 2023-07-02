
import uuid
from django.db import models
from apps.user.models import User
from django.forms import model_to_dict
import random
from collections import defaultdict

#from apps.srea.utils.encryption_util import *
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.shortcuts import render, redirect, get_object_or_404
##############################PARA EL TEST##################################
class Quiz(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    name =  models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    attempts = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    start_date = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
    time_limit = models.TimeField(default='01:00:00', auto_now=False, auto_now_add=False, blank=False, null=False)
    state =  models.BooleanField(default=True, blank=False, null=False)
    createdAt = models.DateTimeField('CreatedAt', auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField('UpdatedAt', auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'quiz'
        verbose_name = 'quiz'
        verbose_name_plural = 'quizzes'
        ordering = ['name', 'createdAt', 'start_date']

    def __str__(self):
        return self.name
    
    def get_questions(self):
        return self.quiz_question.all()
    

class Question(models.Model):
    S_Text = 'T'
    S_Single = 'S'
    S_Multiple = 'M'
    CHOICE_TYPE = ((S_Text, 'Text'), (S_Single, 'Single'), (S_Multiple, 'Multiple'))
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    statement = models.TextField(blank=False, null=False)
    type_question = models.CharField(max_length=1, choices=CHOICE_TYPE, default=S_Single)
    state =  models.BooleanField(default=True, blank=False, null=False)
    createdAt = models.DateTimeField('CreatedAt', auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField('UpdatedAt', auto_now=True, auto_now_add=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_question")

    class Meta:
        db_table = 'question'
        verbose_name = 'question'
        verbose_name_plural = 'questions'
        ordering = ['quiz', 'statement', 'createdAt', ]

    def __str__(self):
        return self.statement
    

    def get_answer(self):
        return self.question_answer.all()

class Answer(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    text = models.TextField(blank=False, null=False)
    learning_style = models.ForeignKey("srea.CatalogItem", on_delete=models.CASCADE)
    state =  models.BooleanField(default=True, blank=False, null=False)
    createdAt = models.DateTimeField('CreatedAt', auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField('UpdatedAt', auto_now=True, auto_now_add=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answer')


    class Meta:
        db_table = 'answer'
        verbose_name = 'answer'
        verbose_name_plural = 'answers'
        ordering = ['question', 'text', 'createdAt', 'learning_style' ]

    def __str__(self):
        return self.text
    

class UserResponse(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    attempt = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    state =  models.BooleanField(default=True, blank=False, null=False)
    createdAt = models.DateTimeField('CreatedAt', auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField('UpdatedAt', auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_response")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)




    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        #item['quiz']=self.get_quiz()
        #item['uuid']=self.get_uuid()
        #item['user']=self.get_quiz()
        return item

    class Meta:
        db_table = 'user_response'
        verbose_name = 'user_response'
        verbose_name_plural = 'user_responses'
        ordering = ['user', 'quiz', 'question', 'answer']



    def __str__(self):
        return f"Response: {self.answer.text} (User: {self.user.username})"
    


#from apps.srea.models import Unidad


    