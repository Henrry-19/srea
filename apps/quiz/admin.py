from django.contrib import admin
from apps.quiz.models import *

# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'description', 'attempts', 'start_date', 'end_date', 'time_limit')
    list_filter = ('name', 'external_id', 'start_date',)
    search_fields = ('name', 'external_id', 'start_date',)
    inlines = [QuestionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'statement', 'type_question', 'state', 'quiz', 'createdAt', 'updatedAt')
    list_filter = ('statement', 'external_id', 'type_question',)
    search_fields = ('statement', 'external_id', 'type_question', 'quiz')
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'text', 'learning_style', 'state', 'question', 'createdAt', 'updatedAt')
    list_filter = ('text', 'external_id', 'learning_style',)
    search_fields = ('text', 'external_id', 'learning_style', 'question')



class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'attempt', 'state', 'user', 'quiz', 'question', 'answer', 'createdAt', 'updatedAt')
    list_filter = ('attempt', 'state', 'user',)
    search_fields = ('attempt', 'state', 'user', 'quiz')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
