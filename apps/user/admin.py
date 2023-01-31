from django.contrib import admin
from apps.user.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['id',"first_name", 'last_name','username','email', 'imagen','ficha', 'get_groups']
    search_fields = ['username']
    list_filter = ['date_joined']
    ordering = ['date_joined']
    def get_groups(self, obj):
        return "\n".join([str(g) for g in obj.groups.all()])

admin.site.register(User, UserAdmin)
admin.site.register(Ficha)
admin.site.register(Indicacion)