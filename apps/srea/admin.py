from django.contrib import admin
from .models import *
admin.site.site_header = 'Admin SREA'
admin.site.index_title = 'Panel de Control'


class CatalogItemInline(admin.TabularInline):
    model = CatalogItem
    extra = 1


class CatalagAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'active', 'createdAt', 'updatedAt')
    inlines = [CatalogItemInline]


class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'active', 'catalog', 'createdAt', 'updatedAt')
    list_filter = ('name', 'active')
    search_fields = ('name', 'external_id', 'catalog__name')


# ASIGNATURAS
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['nombre','detalle', 'imagen']
    search_fields = ['nombre']
    

class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['user','asignatura']
    search_fields = ['user']


admin.site.register(Catalog, CatalagAdmin)
admin.site.register(CatalogItem, CatalogItemAdmin)
admin.site.register(Facultad)
admin.site.register(Ciclo)
admin.site.register(Carrera)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(Unidad)
admin.site.register(MensajenAsignatura)
admin.site.register(FileUploaded)
admin.site.register(UnidadQuiz)
admin.site.register(SubirArchivos)
admin.site.register(UserQuiz)






