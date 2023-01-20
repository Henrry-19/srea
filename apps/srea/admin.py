from django.contrib import admin
from .models import *

admin.site.site_header = 'Admin SREA'
admin.site.index_title = 'Panel de Control'

# ASIGNATURAS
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['nombre','detalle', 'imagen']
    search_fields = ['nombre']
    
admin.site.register(Asignatura, AsignaturaAdmin)

class RespuestaInline(admin.StackedInline):
    model = Respuesta
    extra=0

class RespuestaAdmin(admin.ModelAdmin):
    inlines = [RespuestaInline] 
#    search_fields = ['nombre']


# Register your models here.
#admin.site.register(Usuario)
#-------------------------------------
#admin.site.register(FichaInformacion)
#admin.site.register(Indicacion)

#admin.site.register(Nivel)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['user','asignatura']
    search_fields = ['user']
    
admin.site.register(Matricula)
admin.site.register(Test)
admin.site.register(Pregunta, RespuestaAdmin)
admin.site.register(Respuesta)






