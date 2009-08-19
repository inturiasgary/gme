from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'perfiles.views.perfiles', name='lista_perfil'),
    url(r'^(?P<username>[\w]+)/$', 'perfiles.views.perfil', name='detalle_perfil'),
    # url(r'^username_autocomplete/$', 'profiles.views.username_autocomplete', name='profile_username_autocomplete'),
)