from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^$','microblog.views.index', name="mic_index"),
                       #adicionar entradas
                       url(r'^e/adicionar/$', 'microblog.views.editar_entrada', name="mic_adicionar"),
                       #conecciones
                       url(r'^c/buscar/$', 'microblog.views.buscar_amigo', name="mic_buscaramigo"),
                       url(r'^c/adicionar/(?P<username>[\w_-]+)/$', 'microblog.views.conexion_adicionar', name="mic_cadicionar"),
                       
                       url(r'^c/(?P<conexion_id>\d+)/aceptar/$', 'microblog.views.conexion_aceptar',name="mic_aceptar"),
                       url(r'^c/(?P<conexion_id>\d+)/bloquear/$', 'microblog.views.conexion_bloquear',name="mic_bloquear"),
                       url(r'^c/(?P<conexion_id>\d+)/eliminar/$', 'microblog.views.conexion_eliminar', name="mic_eliminar"),
                       #detalle de usuarios
                       url(r'^u/(?P<username>[\w_-]+)/$', 'microblog.views.detalle_usuario', name="detalle_usuario"),
)
