from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    url(r'^repo/$', 'repositorio.views.index', name="repo_index"),
    #url(r'^(?P<nombre_repo>[\w]+)/$', 'repositorio.views.repo', name='detalle_repo'),
    url(r'^adicionar/$', 'repositorio.views.editar_repositorio', name="rep_adicionar"),
    url(r'^detalle/(\w+)/$', 'repositorio.views.repo', name="repo_detalle"),
    url(r'^detalle/(\w+)/miembros/$','repositorio.views.repo_miembros', name="repo_miembros"),
    url(r'^save/(\w+)/$', 'repositorio.views.repo_save_page', name="repo_save_page"),
    url(r'^find/$','repositorio.views.search_repositorio',name="search_repositorio"),
)
urlpatterns += patterns('',    
    url(r'^editrepositorio/$', 'repositorio.views.edit_repositorio', name='edit_repositorio'),
    url(r'^deleterepositorio/$','repositorio.views.delete_repositorio', name="delete_repositorio"),
    # ajax validation
    #(r'^validate/$', 'ajax_validation.views.validate', {'form_class': RegistroForm}, 'registro_form_validate'),
)
