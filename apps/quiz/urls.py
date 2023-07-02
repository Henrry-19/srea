from django.contrib import admin
from django.urls import *



from django.conf import settings
from django.conf.urls.static import static

#----------------------------------------------
from apps.quiz.vistas.categoria import*
from apps.quiz.views import*

app_name = "apps.quiz"

urlpatterns = [

#---------------------------Nueva versión de cuestionario---------------------------------------
    path('srea/categoria/',CategoriaListView.as_view(), name="categoria"), #presentar
    path('cargar/archivo/', FileLoadedCreateView.as_view(), name="archivo_cargado_crear2"),
    path('list/', ListQuiz.as_view(), name="listar"),
    path('unidades/cargar/<str:asignatura_id>/', CargarQuiz, name="archivo_cargado_crear"),
   
    ################################################################################################
    path('resultado_estilos/<int:quiz_id>',presentarResultado, name="presentar_resultado_quiz"), #presentar
    path('resultado_todos_resultados/<asignatura_id>', presentarTodosResultado, name="presentar_tod_resultado"),
    ######################################USUARIO###################################################
    path('resultado_usuario/<int:user_id>',presentarResultadoUsuario2, name="presentar_resultado_usuario"),

    path('docente_quiz/<asignatura_id>/', presentarQuizDocente, name="docente_quiz"),
    
]

