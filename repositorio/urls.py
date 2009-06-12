from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^repo/$', 'repositorio.views.index', name="repo_index"),
    #url(r'^(?P<nombre_repo>[\w]+)/$', 'repositorio.views.repo', name='detalle_repo'),
    url(r'^adicionar/$', 'repositorio.views.editar_repositorio', name="rep_adicionar"),
    url(r'^(\w+)/$', 'repositorio.views.repo', name="repo_detalle"),
    # ajax validation
    #(r'^validate/$', 'ajax_validation.views.validate', {'form_class': RegistroForm}, 'registro_form_validate'),
)
