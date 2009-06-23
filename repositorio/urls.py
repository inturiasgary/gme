from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from views import *

urlpatterns = patterns('',
    url(r'^repo/$', 'repositorio.views.index', name="repo_index"),
    #url(r'^(?P<nombre_repo>[\w]+)/$', 'repositorio.views.repo', name='detalle_repo'),
    url(r'^adicionar/$', 'repositorio.views.editar_repositorio', name="rep_adicionar"),
    url(r'^detalle/(\w+)/$', 'repositorio.views.repo', name="repo_detalle"),
    url(r'^save/(\w+)/$', 'repositorio.views.repo_save_page', name="repo_save_page"),
)
urlpatterns += patterns('',    
    url(r'^editrepositorio/$', edit_repositorio, name='edit_repositorio'),
    url(r'^deleterepositorio/$','repositorio.views.delete_repositorio', name="delete_repositorio"),
    # ajax validation
    #(r'^validate/$', 'ajax_validation.views.validate', {'form_class': RegistroForm}, 'registro_form_validate'),
)
