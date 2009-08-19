from django.conf.urls.defaults import *
from cuenta.forms import *

urlpatterns = patterns('',
    url(r'^email/$', 'cuenta.views.email', name="acct_email"),
    url(r'^registro/$', 'cuenta.views.registro', name="acct_registro"),
    url(r'^login/$', 'cuenta.views.login', name="acct_login"),
    url(r'^password_change/$', 'cuenta.views.password_change', name="acct_passwd"),
    url(r'^password_reset/$', 'cuenta.views.password_reset', name="acct_passwd_reset"),
    url(r'^timezone/$', 'cuenta.views.timezone_change', name="acct_timezone_change"),
    url(r'^language/$', 'cuenta.views.language_change', name="acct_language_change"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"template_name": "cuenta/logout.html"}, name="acct_logout"),
    url(r'^confirm_email/(\w+)/$', 'emailconfirmation.views.confirm_email', name="acct_confirm_email"),
    # ajax validation
    (r'^validate/$', 'ajax_validation.views.validate', {'form_class': RegistroForm}, 'registro_form_validate'),
)
