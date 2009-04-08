from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader  import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from forms import RegistracionForm
from django.contrib.auth.decorators import login_required

def index(request):
    MICROBLOG_URL_BASE = app_settings.MICROBLOG_URL_BASE
    
    if request.user.is_authenticated():
        noticias   = request.usuario.anuncios_recibidos.all()[:app_settings.MICROBLOG_ENTRIES_LIMIT]
        conexiones = request.usuario.conexiones_desde.all()
        conexiones_mostrar_acciones = True
        
        return render_to_response(
                "/index.html",
                locals(),
                context_instanceRequestContext(request),
        )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
