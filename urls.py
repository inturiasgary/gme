from django.conf.urls.defaults import *
from django.contrib import admin
from microblog.views import logout_page
from django.conf import settings
from django.views.generic.simple import direct_to_template
import os 

admin.autodiscover()

urlpatterns = patterns('',
    # XML-RPC
     url(r'^$', direct_to_template, {"template":"homepage.html"}, name="home"),
     url(r'^xml_rpc_srv/', 'gme.xmlrpc.rpc_handler'),
     url(r'^login/$', 'django.contrib.auth.views.login'),
     url(r'^logout/$',logout_page),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^account/', include('account.urls')),
     url(r'^profiles/', include('profiles.urls')),
     
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^site_media/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),
                            )
    # Example:
    # (r'^gme/', include('gme.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    

