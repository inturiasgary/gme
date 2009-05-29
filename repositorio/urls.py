from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^repo/$', 'repositorio.views.index', name="repo_index"),
    # ajax validation
    #(r'^validate/$', 'ajax_validation.views.validate', {'form_class': RegistroForm}, 'registro_form_validate'),
)
