from django.contrib.admin.options import ModelAdmin
from django.contrib import admin

from models import Anuncio, Conexion

class AdminAnuncio(ModelAdmin):
    list_display = ('usuario', 'fecha', 'contenido')

class AdminConexion(ModelAdmin):
    list_display = ('usuario', 'amigo', 'estado', 'fecha')

admin.site.register(Anuncio, AdminAnuncio)
admin.site.register(Conexion, AdminConexion)
