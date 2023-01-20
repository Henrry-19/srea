from django.urls import path
from .vistas.indicacion import *
from .vistas.asignatura import *
from .vistas.matricula import *
from .vistas.nivel import *
from .vistas.test import *
from .vistas.pregunta import *
from .vistas.respuesta import *
from .vistas.curso import *

from .vistas.index import *

from django.contrib.auth.decorators import login_required

app_name="apps.srea" #Variable que me permite decir como se va a llamar la ruta que se va a concatenar con la otra ruta absoluta

urlpatterns = [
#-------------------------------home---------------------------------------#
path('index1/',IndexView.as_view(), name="index1"),

#-------------------------Usuario---------------------------------------
#    path('u_lista/',(UsuarioListView.as_view()), name="principal"),
#    path('usuario/', (UsuarioCreateView.as_view()), name="usuario"),
#    path('u_lista/u_usuario/<int:pk>/', UsuarioUpdateView.as_view(), name="u_usuario"),
#    path('u_lista/d_usuario/<int:pk>/', UsuarioDeleteView.as_view(), name="d_usuario"),
#-------------------------Reporte---------------------------------------
#    path('r_lista/',ReporteListView.as_view(), name="p_reporte"), #principal_reporte
#    path('r_lista/r_lista_pdf/',ReporteListPdf.as_view(), name="reporte_pdf"), #principal_reporte
#    path('reporte/',ReporteCreateView.as_view(), name="reporte"), #crear reporte
#    path('r_lista/updateR/<int:pk>/', ReporteUpdateView.as_view(), name="update_reporte"),
#    path('r_lista/deleteR/<int:pk>/', ReporteDeleteView.as_view(), name="delete_reporte"),
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
#-------------------------Matrícula-----------------------------------------
    path('evaluar/',MatriculaListView.as_view(), name="matricula"),
#    path('listar/',ListarMatriculaListView.as_view(), name="p_matricula"),
#-------------------------Test-----------------------------------------
    path('t_lista/',TestListView.as_view(), name="test"), #principal_test
#    path('test/',TestCreateView.as_view(), name="test"), #crear test
#    path('t_lista/updateT/<int:pk>/',TestUpdateView.as_view(), name="update_test"),
#    path('t_lista/deleteT/<int:pk>/',TestDeleteView.as_view(), name="delete_test"),
#-------------------------Pregunta-----------------------------------------
    path('p_lista/',PreguntaListView.as_view(), name="pregunta"), #Listar preguntas
    path('pregunta/',PreguntaCreateView.as_view(), name="r_pregunta"), #crear ficha
    path('p_lista/u_pregunta/<int:pk>/', PreguntaUpdateView.as_view(), name="u_pregunta"),
    path('p_lista/d_pregunta/<int:pk>/', PreguntaDeleteView.as_view(), name="d_pregunta"),

    
]


