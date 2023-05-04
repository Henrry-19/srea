from django.contrib import admin
from django.urls import *
from apps.quiz.vistas.cuestionario import *
from apps.quiz.vistas.pregunta import *
from apps.quiz.vistas.attempter import *

from django.conf import settings
from django.conf.urls.static import static

#----------------------------------------------
from apps.quiz.vistas.categoria import*
from apps.quiz.views import*

app_name = "apps.quiz"

urlpatterns = [
    #path('t_lista/',CuestionarioListView.as_view(), name="test"),
    #path('cuestionario/',CuestionarioView.as_view(), name="main-view"),
   # path('cuestionario/<pk>/',cuestionario_view, name="cuestionario-view"),
    #path('cuestionario/<pk>/save/',save_cuestionario_view, name="save-view"),
    #path('cuestionario/<pk>/data',cuestionario_data_view, name="cuestionario-data-view"),

    #-------------------------Pregunta-----------------------------------------
   # path('p_lista/',PreguntaListView.as_view(), name="pregunta"), #Listar preguntas
   # path('pregunta/',PreguntaCreateView.as_view(), name="r_pregunta"), #crear pregunta
   # path('p_lista/u_pregunta/<int:pk>/', PreguntaUpdateView.as_view(), name="u_pregunta"),
   # path('p_lista/d_pregunta/<int:pk>/', PreguntaDeleteView.as_view(), name="d_pregunta"),
    #path('api/get_test/', get_test, name="get_test"),


 #-------------------------Respuesta-----------------------------------------
   # path('respuesta/',RespuestaCreateView.as_view(), name="r_respuesta"), #crear respuesta  

#---------------------------Nueva versión de cuestionario---------------------------------------
    path('srea/categoria/',CategoriaListView.as_view(), name="categoria"), #presentar
    #path('act-quiz/<int:pk>/', QuizUpdateView.as_view(), name='act-quiz')

]

