from django.contrib import admin
from .models import *
from .forms import  ElegirInlineFormset
admin.site.register(PreguntasRespondidas)
admin.site.register(ElegirRespuesta)


# Register your models here.

admin.site.register(Cuenta)
admin.site.register(Usuario)
admin.site.register(Reporte)
admin.site.register(FichaInformacion)
admin.site.register(Indicacion)
admin.site.register(Test)
admin.site.register(Nivel)
admin.site.register(Asignatura)
admin.site.register(User)


class ElegirRespuestaInline(admin.TabularInline):
    model= ElegirRespuesta
    can_delete = False
    max_num= ElegirRespuesta.MAXIMO_RESPUESTA
    min_num= ElegirRespuesta.MAXIMO_RESPUESTA
    formset = ElegirInlineFormset
    




class PreguntaAdmin(admin.ModelAdmin):
    model= Pregunta
    inlines=(ElegirRespuestaInline,)
    list_display = ['texto',]
    search_fields = ['texto','preguntas_texto']

class PreguntasRespondidasAmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidas


admin.site.register(Pregunta, PreguntaAdmin)
