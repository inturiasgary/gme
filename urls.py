from django.conf.urls.defaults import *
from django.contrib import admin
from microblog.views import logout_page

admin.autodiscover()

urlpatterns = patterns('',
    # XML-RPC
     (r'^xml_rpc_srv/', 'gme.xmlrpc.rpc_handler'),
     url(r'^login/$', 'django.contrib.auth.views.login'),
     url(r'^logout/$',logout_page),
     url(r'^admin/', include(admin.site.urls)),
)

    # Example:
    # (r'^gme/', include('gme.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    

