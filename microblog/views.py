from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from templatetags import microblog_utils
import app_settings
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader  import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from models import Entrada, Conexion, CONEXION_ESPERANDO, CONEXION_BLOQUEADA, CONEXION_ACEPTADA
from django.contrib.auth.decorators import login_required

from forms import FormEntrada, FormEncontrarAmigo, FormConexion

def index(request):
    MICROBLOG_URL_BASE = app_settings.MICROBLOG_URL_BASE
    
    form_entrada  = FormEntrada()
    form_conectar = FormEncontrarAmigo()
    
    if request.user.is_authenticated():
        entradas   = request.user.entradas_recibidos.all()[:app_settings.MICROBLOG_ENTRIES_LIMIT]
        conexiones = request.user.conexiones_desde.all()
        conexiones_mostrar_acciones = True
        
    return render_to_response(
        "microblog/index.html",
        locals(),
        context_instance=RequestContext(request),
        )


@login_required
def editar_entrada(request, entrada_id=None):
    MICROBLOG_URL_BASE = app_settings.MICROBLOG_URL_BASE
    
    if entrada_id:
        entrada = get_object_or_404(Entrada, id=entrada_id) #para editar
    else:
        entrada = None #para la creacion 
        
    if request.POST:
        form = FormEntrada(request.POST, instance=entrada)
        
        if form.is_valid():
            entrada = form.save(False) #asignamos los valores, sin guardar aun
            entrada.user = request.user #asignamos el valor user de la entrada con el actual uausrio
            entrada.save() #salvamos la entrada
            
            if entrada:
                return HttpResponseRedirect(app_settings.MICROBLOG_URL_BASE)
    else:
        form = FormEntrada(instance=entrada)
            
    return render_to_response(
        'microblog/editar_entrada.html',
        locals(),
        context_instance=RequestContext(request),
        )

def buscar_amigo(request):
    MICROBLOG_URL_BASE = app_settings.MICROBLOG_URL_BASE
    
    if request.GET:
        form = FormEncontrarAmigo(request.GET)
        
        if form.is_valid():
            usuarios_encontrados = form.encontrar()
            
            if usuarios_encontrados.count() == 1:
                return HttpResponseRedirect(usuarios_encontrados[0].get_absolute_url())
    else:
        form = FormEncontrarAmigo()
        
    return render_to_response(
        'microblog/encontrar_amigo.html',
        locals(),
        context_instance = RequestContext(request),
        )

@login_required
def conexion_adicionar(request, username):
    amigo = get_object_or_404(User, username=username)
    
    conexion, new = Conexion.objects.get_or_create(
        user=request.user,
        amigo = amigo,
        defaults={
            'estado': CONEXION_ACEPTADA,
        }
    )
    
    if not new:
        
        request.user.message_set.create(meesage=_('Tu ya estas conectado con el usuario!'))
    return HttpResponseRedirect(app_settings.MICROBLOG_URL_BASE)

@login_required
def conexion_aceptar(request, conexion_id):
    conexion = get_object_or_404(Conexion, id=conexion_id)
    conexion.estado = CONEXION_ACEPTADA
    conexion.save()
    
    request.user.message_set.create(message=_('Conexion aceptada!'))
    
    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER', app_settings.MICROBLOG_URL_BASE)
        )

@login_required
def conexion_bloquear(request, conexion_id):
    conexion = get_object_or_404(Conexion, id=conexion_id)
    conexion.estado = CONEXION_BLOQUEADA
    conexion.save()
    
    request.user.message_set.create(message=_('Conexion bloqueada!'))
    
    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER', app_settings.MICROBLOG_URL_BASE)
        )

@login_required
def conexion_eliminar(request, conexion_id):
    conexion = get_object_or_404(Conexion, id=conexion_id)
    conexion.delete()
    
    request.user.message_set.create(message=_('Conexion Eliminida!'))
    
    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER', app_settings.MICROBLOG_URL_BASE)
        )

def detalle_usuario(request, username):
    MICROBLOG_URL_BASE =app_settings.MICROBLOG_URL_BASE
    
    usuario_actual = get_object_or_404(User, username=username)
    conexiones = usuario_actual.conexiones_desde.filter(estado=CONEXION_ACEPTADA)
    
    return render_to_response(
        'microblog/detalles_usuario.html',
        locals(),
        context_instance=RequestContext(request),
        )