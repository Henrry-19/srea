from django.urls import path
from .vistas.indicacion import *
from .vistas.asignatura import *
from .vistas.curso import *
from .vistas.nivel import *
from .vistas.curso_test import *
from .vistas.unidad import *

from .vistas.index import *

######################################################
from django.views import View
######################################################

from django.contrib.auth.decorators import login_required

app_name="apps.srea" #Variable que me permite decir como se va a llamar la ruta que se va a concatenar con la otra ruta absoluta

urlpatterns = [
#-------------------------------home---------------------------------------#
path('index1/',IndexView.as_view(), name="index1"),
#path('index2/',IndexViewAsignatura.as_view(), name="index_asignatura"),
#-------------------------Indicacion-----------------------------------------
#    path('i_lista/',IndicacionListView.as_view(), name="p_indicacion"), #principal_indicacion
#    path('indicacion/',IndicacionCreateView.as_view(), name="indicacion"), #crear indicacion
#    path('i_lista/updateI/<int:pk>/', IndicacionUpdateView.as_view(), name="update_indicacion"),
#   path('i_lista/deleteI/<int:pk>/', IndicacionDeleteView.as_view(), name="delete_indicacion"),
#-------------------------Asignatura-----------------------------------------
    path('a_lista/',AsignaturaListView.as_view(), name="p_asignatura"), #principal_asignatura
    path('asignatura/',AsignaturaCreateView.as_view(), name="asignatura"), #crear asignatura
    path('a_lista/u_asignatura/<int:pk>/', AsignaturaUpdateView.as_view(), name="u_asignatura"),
    path('a_lista/d_asignatura/<int:pk>/', AsignaturaDeleteView.as_view(), name="d_asignatura"),
    #######################################Acceder##############################################
#-------------------------Unidad-----------------------------------------
    #path('u_lista/',UnidadListView.as_view(), name="p_unidad"), #principal_unidad
    #-------------Unidades----------------#UnidadesListView
    path('u_unidad/',UnidadesListView.as_view(), name="unidad"), #principal_unidad
    path('unidad/',UnidadCreateView.as_view(), name="unidad_create"), #crear asignatura
    path('u_unidad/act_unidad/<int:pk>/', UnidadUpdateView.as_view(), name="act_unidad"),
    path('u_unidad/d_unidad/<int:pk>/', UnidadDeleteView.as_view(), name="delete_unidad"),
    #---------------Primera---------------------------- PrimeraUnidadListView
    path('primera_unidad/',PrimeraUnidadListView.as_view(), name="primera_unidad"), #principal_unidad

#-------------------------Curso-----------------------------------------
    path('evaluar/',CursoListView.as_view(), name="curso"),
    path('matricula/',CursoCreateView.as_view(), name="r_curso"),
    path('matricula/u_matricula/<int:pk>/', CursoUpdateView.as_view(), name="u_curso"),
    path('matricula/d_matricula/<int:pk>/', CursoDeleteView.as_view(), name="d_curso"),
]


