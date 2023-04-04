from django.urls import path
from .vistas.indicacion import *
from .vistas.asignatura import *
from .vistas.curso import *
from .vistas.nivel import *
from .vistas.curso_test import *
from .vistas.unidad import *

from apps.quiz.views import*

from .vistas.index import *

######################################################
from django.views import View
######################################################

from django.contrib.auth.decorators import login_required

app_name="apps.srea" #Variable que me permite decir como se va a llamar la ruta que se va a concatenar con la otra ruta absoluta

urlpatterns = [
#-------------------------------home---------------------------------------#
    path('index1/',IndexView.as_view(), name="index1"),
#path('index1/', index, name="index1"),
#path('index2/',IndexViewAsignatura.as_view(), name="index_asignatura"),
#-------------------------Indicacion-----------------------------------------
#    path('i_lista/',IndicacionListView.as_view(), name="p_indicacion"), #principal_indicacion
#    path('indicacion/',IndicacionCreateView.as_view(), name="indicacion"), #crear indicacion
#    path('i_lista/updateI/<int:pk>/', IndicacionUpdateView.as_view(), name="update_indicacion"),
#   path('i_lista/deleteI/<int:pk>/', IndicacionDeleteView.as_view(), name="delete_indicacion"),
#-------------------------Asignatura-----------------------------------------
    path('a_lista/',AsignaturaListView.as_view(), name="p_asignatura"), #principal_asignatura
    #path('a_lista/',MyCourses, name="p_asignatura"), #principal_asignatura
    path('asignatura/',AsignaturaCreateView.as_view(), name="asignatura"), #crear asignatura
    path('ad_asignatura/<str:pk>/', AsignaturaUpdateView.as_view(), name="u_asignatura"),
    path('d_asignatura/<str:pk>/', AsignaturaDeleteView.as_view(), name="d_asignatura"),
    #######################################Acceder##############################################
    path('asignatura/<str:asignatura_id>/', AsignaturaDetail, name='course'),

    path('<str:asignatura_id>/matricula-lista/<int:user_id>/', MatricularLista, name='matricula-lista'),
    path('<asignatura_id>/enroll/<int:user_id>/matricular', Enroll, name='enroll'),
    #ListarEstudiantes
    path('estudiantes/<str:asignatura_id>/', ListarEstudiantes, name='estudiantes'),
#-------------------------Unidad-----------------------------------------
    #path('u_lista/',UnidadListView.as_view(), name="p_unidad"), #principal_unidad
    #-------------Unidades----------------#UnidadesListView
    #path('u_unidad/',UnidadesListView.as_view(), name="unidad"), #principal_unidad
    #path('<asignatura_id>/unidad',NewModule, name="unidad"), #crear asignatura
    #path('u_unidad/d_unidad/<int:pk>/', UnidadDeleteView.as_view(), name="delete_unidad"),
    #---------------Primera---------------------------- PrimeraUnidadListView
    #path('primera_unidad/',PrimeraUnidadListView.as_view(), name="primera_unidad"), #principal_unidad
    path('<asignatura_id>/unidades',AsignaturaUnidades, name="primeraU"),
    path('<asignatura_id>/unidades/newunidades',NewModule, name="unidad"), #crear unidad
    path('<asignatura_id>/<int:unidad_id>/unidades/act_unidad/', EditMudule, name="act-unidad"),
    path('u_unidad/d_unidad/<int:pk>/', UnidadDeleteView.as_view(), name="delete_unidad"),
#-------------------------Ciclo-----------------------------------------
    #path('evaluar/',CursoListView.as_view(), name="curso"),
    #path('ciclo/',CursoListView.as_view(), name="curso"),
    path('ciclo/',CursoListView.as_view(), name="curso"),
    path('matricula/',CursoCreateView.as_view(), name="r_curso"),
    path('matricula/u_matricula/<int:pk>/', CursoUpdateView.as_view(), name="u_curso"),
    path('matricula/d_matricula/<int:pk>/', CursoDeleteView.as_view(), name="d_curso"),

    #-----------------------------------QUIZ--------------------------------------------------

    path('<asignatura_id>/unidades/<unidad_id>/quiz/newquiz', NewQuiz, name='new-quiz'),
    
    path('<asignatura_id>/unidades/<unidad_id>/quiz/<int:quiz_id>/newquestion', NewQuestion, name='new-question'),
    path('<asignatura_id>/unidades/<unidad_id>/quiz/<quiz_id>/', QuizDetail, name='quiz-detail'),
    path('<asignatura_id>/unidades/<unidad_id>/quiz/<quiz_id>/take', TakeQuiz, name='take-quiz'),
    path('<asignatura_id>/unidades/<unidad_id>/quiz/<quiz_id>/take/submit', SubmitAttempt, name='submit-quiz'),
    path('<asignatura_id>/unidades/<unidad_id>/quiz/<quiz_id>/<attempt_id>/result', AttemptDetail, name='attempt-detail'),


]


