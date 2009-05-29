from django.contrib.admin.options import ModelAdmin
from django.contrib import admin

from models import Repositorio, Miembro, Topico, Commit

class AdminRepositorio(ModelAdmin):
    list_display = ('creador', 'nombre', 'fecha', 'borrado')

class AdminMiembro(ModelAdmin):
    list_display = ('usuario', 'activo', 'repositorio')
    
class AdminTopico(ModelAdmin):
    list_display = ('repositorio', 'titulo')
    
class AdminCommit(ModelAdmin):
    list_display = ('usuario','fecha', 'descripcion')

admin.site.register(Repositorio, AdminRepositorio)
admin.site.register(Miembro, AdminMiembro)
admin.site.register(Topico, AdminTopico)
admin.site.register(Commit, AdminCommit)
