from django.contrib import admin
from apps.quiz.models import *
from .models import *
admin.site.site_header = 'Admin SREA'
admin.site.index_title = 'Panel de Control'

# ASIGNATURAS
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['nombre','detalle', 'imagen']
    search_fields = ['nombre']
    
admin.site.register(Asignatura, AsignaturaAdmin)

admin.site.register(Unidad)
#admin.site.register(Cuestionario)

admin.site.register(Answer)

#admin.site.register(Resultado)



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 20

class AnswerInline(admin.TabularInline):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Quizzes)
admin.site.register(Attempt)
admin.site.register(Attempter)
admin.site.register(Completion)
# Register your models here.
#admin.site.register(Usuario)
#-------------------------------------
#admin.site.register(FichaInformacion)
#admin.site.register(Indicacion)

#admin.site.register(Nivel)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['user','asignatura']
    search_fields = ['user']

admin.site.register(Facultad)
admin.site.register(Ciclo)
admin.site.register(Carrera)
#admin.site.register(Pregunta, PreguntaAdmin)
#admin.site.register(Pregunta)
#admin.site.register(Respuesta)






