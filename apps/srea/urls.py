from django.urls import path
from .vistas.asignatura import *
from .vistas.curso import *
from .vistas.unidad import *
from .vistas.catalogo import *
from .vistas.catalago_item import *
from .vistas.mensaje import *
from .vistas.user_quiz import *

from apps.quiz.views import*
from .vistas.file import *

######################################################
from django.views import View
######################################################

from django.contrib.auth.decorators import login_required

app_name="apps.srea" #Variable que me permite decir como se va a llamar la ruta que se va a concatenar con la otra ruta absoluta

urlpatterns = [
#-------------------------------home---------------------------------------#
    path('index1/',presentarResultadoUsuario, name="index1"), #IndexView.as_view()--->Revisar este método
   

#-------------------------Asignatura-----------------------------------------
    path('a_lista/',AsignaturaListView.as_view(), name="p_asignatura"), #principal_asignatura
    path('asignatura/',AsignaturaCreateView.as_view(), name="asignatura"), #crear asignatura
    path('ad_asignatura/<str:asignatura_id>/', AsignaturaUpdateView, name="u_asignatura"),
    path('d_asignatura/<str:pk>/', AsignaturaDeleteView.as_view(), name="d_asignatura"),
    #######################################Acceder a cada asignatura##############################################
    path('asignatura/<str:asignatura_id>/user/', AsignaturaDetail, name='course'),

    path('<str:asignatura_id>/matricula-lista/<int:user_id>/', MatricularLista, name='matricula-lista'),
    path('<asignatura_id>/enroll/<int:user_id>/matricular', Matricular, name='enroll'),
    #ListarEstudiantes
    path('estudiantes/<str:asignatura_id>/', ListarEstudiantes, name='estudiantes'),
#-------------------------Unidad-----------------------------------------WS
    path('<asignatura_id>/unidades/',AsignaturaUnidades, name="primeraU"),
    path('<asignatura_id>/unidades/newunidades',NewModule, name="unidad"), #crear unidad
    path('<asignatura_id>/<str:unidad_id>/unidades/act_unidad/', EditMudule, name="act-unidad"),
    path('u_unidad/d_unidad/<str:pk>/', UnidadDeleteView.as_view(), name="delete_unidad"),
#-------------------------Ciclo-----------------------------------------
    path('ciclo/',CursoListView.as_view(), name="curso"),
    path('matricula/',CursoCreateView.as_view(), name="r_curso"),
    path('matricula/u_matricula/<int:pk>/', CursoUpdateView.as_view(), name="u_curso"),
    path('matricula/d_matricula/<int:pk>/', CursoDeleteView.as_view(), name="d_curso"),

    #-----------------------------------QUIZ--------------------------------------------------
    path('registrar/<str:asignatura_id>/unidades/quiz/', RegistrarQuiz,name='registrar-quiz'),
     path('registrar/<str:asignatura_id>/user/quiz/', RegistrarQuizUser,name='registrar-quiz-user'),


    path('<str:asignatura_id>/unidades/<str:unidad_id>/quiz/<int:quiz_id>/take/edit', EditQuiz,name='edit-quiz'),

    path('<str:asignatura_id>/unidades/<str:unidad_id>/quiz/<int:quiz_id>/<int:question_id>/take/edit', EditQuestion,name='edit-question'),
    path('<str:asignatura_id>/unidades/<str:unidad_id>/quiz/<int:quiz_id>/<int:question_id>/<int:answer_id>/take/edit', EditAnswer,name='edit-answer'),    
    
    
    path('<asignatura_id>/unidades/<str:unidad_id>/quiz/<int:external_id>/', QuizDetail, name='quiz-detail'),
    path('<asignatura_id>/unidades/<str:unidad_id>/quiz/<quiz_id>/take', TakeQuiz, name='take-quiz'),
    path('<asignatura_id>/unidades/<str:unidad_id>/quiz/<quiz_id>/take/submit', SubmitAttempt, name='submit-quiz'),

    ##################################Guardar quiz de user#################################################
     path('<asignatura_id>/unidades/quiz/<int:external_id>/', QuizDetailUser, name='quiz-detail-user'),

     path('<asignatura_id>/unidades/quiz/<quiz_id>/take', TakeQuizUser, name='take-quiz-user'),
     path('<asignatura_id>/unidades/quiz/<quiz_id>/take/submit', SubmitAttemptUser, name='submit-quiz-user'),

    ###Usado para Js
    path('<asignatura_id>/unidades/<str:unidad_id>/quiz/<quiz_id>/take/data', TakeQuiz2, name='take-data'),


    #######################################CATALOGO####################################################
    path('catalogo/',CatalogListView.as_view(), name="catalogo"), #presentar
    path('catalogo_crear/',CatalogoCreateView.as_view(), name="catalogo_create"), #crear
    path('catalogo/catalogo_edit/<int:pk>/',CatalogoUpdateView.as_view(), name="catalogo_edit"), #editar
    path('catalogo/catalogo_delete/<int:pk>/', CatalogoDeleteView.as_view(), name="catalogo_delete"),
     #######################################CATALOGO ITEM####################################################
    path('catalogo_item/',CatalogItemListView.as_view(), name="catalogo_item"), #presentar
    path('catalogo_item_crear/',CatalogoItemCreateView.as_view(), name="catalogo_item_create"), #crear
    path('catalogo/catalogo_item_edit/<int:pk>/',CatalogoItemUpdateView.as_view(), name="catalogo_item_edit"), #editar
    path('catalogo/catalogo_item_delete/<int:pk>/', CatalogoItemDeleteView.as_view(), name="catalogo_item_delete"),

    ##########################################MENSAJES#######################################################3
    path('mensaje_asignatura/<asignatura_id>/',MensajeAsignatura, name="mensaje_asignatura"), #presentar
    path('crear_mensaje_asignatura/<asignatura_id>/', MensajeCreate, name='crear_mensajes'),
    path('editar_mensaje_asignatura/<asignatura_id>/<str:mensajenasignatura_id>/', MensajeUpdateView, name='editar_mensajes'),
    path('eliminar_mensaje_asignatura/<str:asignatura_id>/<str:mensajenasignatura_id>/', EliminarMensaje, name='eliminar_mensajes'),
    #Mensaje-------------------->Acceder a cada mensaje
    path('mesajes_asignatura/<str:mensajenasignatura_id>/', MensajeDetail, name='ver_mensajes'),


    #-------------------------File-----------------------------------------
    path('file/',FileListView.as_view(), name="p_file"), #principal_asignatura
]


