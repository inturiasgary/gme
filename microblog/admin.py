from django.contrib.admin.options import ModelAdmin
from django.contrib import admin

from models import Entrada, Conexion

class AdminEntrada(ModelAdmin):
    list_display = ('user', 'fecha', 'contenido')

class AdminConexion(ModelAdmin):
    list_display = ('user', 'amigo', 'estado', 'fecha')

admin.site.register(Entrada, AdminEntrada)
admin.site.register(Conexion, AdminConexion)
