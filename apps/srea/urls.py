from django.urls import path
from .vistas.cuenta import *
from .vistas.usuario import *
from .vistas.reporte import *
from .vistas.indicacion import *
from .vistas.asignatura import *
from .vistas.nivel import *
from .vistas.pregunta import *
from .vistas.test import *
from .vistas.ficha import *
from .vistas.index import *

app_name="apps.srea"

urlpatterns = [
    path('index1/',Index1View.as_view(), name="index1"),#Presenta primera vista de Inicio
    path('index2/',Index2View.as_view(), name="index2"),#Presenta segunda vista de Inicio
    path('cuenta/', CuentaCreateView.as_view(), name="cuenta"),
    path('update/<int:pk>/', CuentaUpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', CuentaDeleteView.as_view(), name="delete"),
#-------------------------Usuario---------------------------------------
    path('u_lista/',UsuarioListView.as_view(), name="principal"),
    path('usuario/', UsuarioCreateView.as_view(), name="usuario"),
    path('u_lista/u_usuario/<int:pk>/', UsuarioUpdateView.as_view(), name="u_usuario"),
    path('u_lista/d_usuario/<int:pk>/', UsuarioDeleteView.as_view(), name="d_usuario"),
#-------------------------Reporte---------------------------------------
    path('r_lista/',ReporteListView.as_view(), name="p_reporte"), #principal_reporte
    path('r_lista/r_lista_pdf/',ReporteListPdf.as_view(), name="reporte_pdf"), #principal_reporte
    path('reporte/',ReporteCreateView.as_view(), name="reporte"), #crear reporte
    path('r_lista/updateR/<int:pk>/', ReporteUpdateView.as_view(), name="update_reporte"),
    path('r_lista/deleteR/<int:pk>/', ReporteDeleteView.as_view(), name="delete_reporte"),
#-------------------------Indicacion-----------------------------------------
    path('i_lista/',IndicacionListView.as_view(), name="p_indicacion"), #principal_indicacion
    path('indicacion/',IndicacionCreateView.as_view(), name="indicacion"), #crear indicacion
    path('i_lista/updateI/<int:pk>/', IndicacionUpdateView.as_view(), name="update_indicacion"),
    path('i_lista/deleteI/<int:pk>/', IndicacionDeleteView.as_view(), name="delete_indicacion"),
#-------------------------Asignatura-----------------------------------------
    path('a_lista/',AsignaturaListView.as_view(), name="p_asignatura"), #principal_asignatura
    path('asignatura/',AsignaturaCreateView.as_view(), name="asignatura"), #crear asignatura
    path('a_lista/u_asignatura/<int:pk>/', AsignaturaUpdateView.as_view(), name="u_asignatura"),
    path('a_lista/d_asignatura/<int:pk>/', AsignaturaDeleteView.as_view(), name="d_asignatura"),

#-------------------------Ficha-----------------------------------------
    path('f_lista/',FichaListView.as_view(), name="p_ficha"), #principal_ficha
    path('ficha/',FichaCreateView.as_view(), name="ficha"), #crear ficha
    path('f_lista/d_ficha/<int:pk>/',FichaDeleteView.as_view(), name="d_ficha"),
     path('f_lista/u_ficha/<int:pk>/',FichaUpdateView.as_view(), name="u_ficha"),
#-------------------------Nivel-----------------------------------------
    path('n_lista/',NivelListView.as_view(), name="p_nivel"), #principal_nivel
    path('nivel/',NivelCreateView.as_view(), name="nivel"), #crear nivel
    path('n_lista/updateN/<int:pk>/',NivelUpdateView.as_view(), name="update_nivel"),
    path('n_lista/deleteN/<int:pk>',NivelDeleteView.as_view(), name="delete_nivel"),
#-------------------------Test-----------------------------------------
    path('t_lista/',TestListView.as_view(), name="p_test"), #principal_test
    path('test/',TestCreateView.as_view(), name="test"), #crear test
    path('t_lista/updateT/<int:pk>/',TestUpdateView.as_view(), name="update_test"),
    path('t_lista/deleteT/<int:pk>/',TestDeleteView.as_view(), name="delete_test"),
#-------------------------Pregunta-----------------------------------------
    #path('p_lista/',HomeUsuario, name="inicio"), #principal_pregunta
    path('registro/',registro, name="registro"), #crear usuario
    path('login2/',login2, name="login2"), #crear login
    path('logout_vista/',logout_vista, name="logout_vista"), #salir de login
    path('HomeUsuario/',HomeUsuario, name="HomeUsuario"), #salir de login
    path('p_lista/',PreguntaListView.as_view(), name="p_pregunta"), #Listar preguntas
    path('pregunta/',PreguntaCreateView.as_view(), name="pregunta"), #crear ficha
    #path('p_lista/',evaluar, name="inicio"), #evaluar preguntas
    path('resultado/<int:pregunta_respondida_pk>/',resultado_pregunta, name='resultado'),
    path('p_lista/u_pregunta/<int:pk>/', PreguntaUpdateView.as_view(), name="u_pregunta"),
    path('p_lista/d_pregunta/<int:pk>/', PreguntaDeleteView.as_view(), name="d_pregunta"),
    #path('p_lista/updateP/<int:pk>/',PreguntaUpdateView.as_view(), name="update_pregunta"),
    #path('p_lista/deleteP/<int:pk>/',PreguntaDeleteView.as_view(), name="delete_pregunta"),


    
]


