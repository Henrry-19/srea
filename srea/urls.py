from django.urls import path
from .views import CuentaDetailView, ReporteCreateView, sreaListView, CuentaCreateView, CuentaUpdateView, CuentaDeleteView
from .views import UsuarioCreateView,UsuarioListView, UsuarioDeleteView,UsuarioUpdateView
from .views import ReporteListView,ReporteListPdf,ReporteUpdateView,ReporteDeleteView
from .views import IndicacionListView,IndicacionCreateView,IndicacionUpdateView,IndicacionDeleteView
from .views import AsignaturaListView,AsignaturaCreateView, AsignaturaUpdateView, AsignaturaDeleteView
from .views import NivelListView, NivelCreateView,NivelUpdateView,NivelDeleteView
from .views import PreguntaListView, PreguntaCreateView, PreguntaDeleteView, PreguntaUpdateView
from .views import TestListView, TestCreateView, TestDeleteView, TestUpdateView

app_name="srea"

urlpatterns = [
    path('',sreaListView.as_view(), name="home"),
    path('cuenta/', CuentaCreateView.as_view(), name="cuenta"),
    path('update/<int:pk>/', CuentaUpdateView.as_view(), name="update"),
    path('delete/<int:pk>', CuentaDeleteView.as_view(), name="delete"),
#-------------------------Usuario---------------------------------------
    path('u_lista/',UsuarioListView.as_view(), name="principal"),
    path('usuario/', UsuarioCreateView.as_view(), name="usuario"),
    path('u_lista/d_usuario/<int:pk>', UsuarioDeleteView.as_view(), name="d_usuario"),
    path('u_lista/u_usuario/<int:pk>/', UsuarioUpdateView.as_view(), name="u_usuario"),
#-------------------------Reporte---------------------------------------
    path('r_lista/',ReporteListView.as_view(), name="p_reporte"), #principal_reporte
    path('r_lista/r_lista_pdf/',ReporteListPdf.as_view(), name="reporte_pdf"), #principal_reporte
    path('reporte/',ReporteCreateView.as_view(), name="reporte"), #crear reporte
    path('r_lista/updateR/<int:pk>/', ReporteUpdateView.as_view(), name="update_reporte"),
    path('r_lista/deleteR/<int:pk>', ReporteDeleteView.as_view(), name="delete_reporte"),
#-------------------------Indicacion-----------------------------------------
    path('i_lista/',IndicacionListView.as_view(), name="p_indicacion"), #principal_indicacion
    path('indicacion/',IndicacionCreateView.as_view(), name="indicacion"), #crear indicacion
    path('i_lista/updateI/<int:pk>/', IndicacionUpdateView.as_view(), name="update_indicacion"),
    path('i_lista/deleteI/<int:pk>', IndicacionDeleteView.as_view(), name="delete_indicacion"),
#-------------------------Asignatura-----------------------------------------
    path('a_lista/',AsignaturaListView.as_view(), name="p_asignatura"), #principal_asignatura
    path('asignatura/',AsignaturaCreateView.as_view(), name="asignatura"), #crear asignatura
    path('a_lista/updateA/<int:pk>/', AsignaturaUpdateView.as_view(), name="update_asignatura"),
    path('a_lista/deleteA/<int:pk>', AsignaturaDeleteView.as_view(), name="delete_asignatura"),
#-------------------------Nivel-----------------------------------------
    path('n_lista/',NivelListView.as_view(), name="p_nivel"), #principal_nivel
    path('nivel/',NivelCreateView.as_view(), name="nivel"), #crear nivel
    path('n_lista/updateN/<int:pk>/',NivelUpdateView.as_view(), name="update_nivel"),
    path('n_lista/deleteN/<int:pk>',NivelDeleteView.as_view(), name="delete_nivel"),
#-------------------------Test-----------------------------------------
    path('t_lista/',TestListView.as_view(), name="p_test"), #principal_test
    path('test/',TestCreateView.as_view(), name="test"), #crear test
    path('t_lista/updateT/<int:pk>/',TestUpdateView.as_view(), name="update_test"),
    path('t_lista/deleteT/<int:pk>',TestDeleteView.as_view(), name="delete_test"),
#-------------------------Pregunta-----------------------------------------
    path('p_lista/',PreguntaListView.as_view(), name="p_pregunta"), #principal_pregunta
    path('pregunta/',PreguntaCreateView.as_view(), name="pregunta"), #crear pregunta
    path('p_lista/updateP/<int:pk>/',PreguntaUpdateView.as_view(), name="update_pregunta"),
    path('p_lista/deleteP/<int:pk>',PreguntaDeleteView.as_view(), name="delete_pregunta"),


    
]


