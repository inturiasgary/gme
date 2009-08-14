from django.contrib.admin.options import ModelAdmin
from django.contrib import admin

from models import Repositorio, Miembro, Topico, Commit, Imagen

class AdminRepositorio(ModelAdmin):
    list_display = ('nombre', 'fecha', 'activo')

class AdminMiembro(ModelAdmin):
    list_display = ('usuario', 'creador','activo', 'repositorio')
    
class AdminTopico(ModelAdmin):
    list_display = ('repositorio', 'titulo')
    
class AdminCommit(ModelAdmin):
    list_display = ('usuario','fecha', 'descripcion')

class AdminImagen(ModelAdmin):
    list_display = ('imagen',)

admin.site.register(Repositorio, AdminRepositorio)
admin.site.register(Miembro, AdminMiembro)
admin.site.register(Topico, AdminTopico)
admin.site.register(Commit, AdminCommit)
admin.site.register(Imagen, AdminImagen)
