from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import FormRepo

def index(request):
    if request.user.is_authenticated():
        #repositorios_mios      = request.user.repositorios_creados.all()
        repositorios_mios = Repositorio.objects.filter(miembros=request.user, miembro__creador=True)
        repositorios_participo = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=True)
        repositorios_pendiente = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=False)
        
    return render_to_response("repositorio/index.html",
                           locals(),
                           context_instance=RequestContext(request),
                           )

def repo(request):
    print "nada"
#@login_required
#def editar_repositorio(request, repositorio_id=None):
    #if repositorio_id:
        #repositorio = get_object_or_404(Repositorio, id=repositorio_id) #para editar el repositorio
        #if repositorio.creador!=request.user:
            #repositorio=None
    #else:
        #repositorio = None
        
    #if request.POST:
        #form = FormRepo(request.POST, instance=repositorio)
        
        #if form.is_valid():
            #repositorio = form.save(False)
            #repositorio.creador = request.user
            #repositorio.save()
            
            #if repositorio:
                #return HttpResponseRedirect(app_settings.MICROBLOG_URL_BASE)
    #else:
        #form = FormRepo(instance=repositorio)
    #return render_to_response(
        #'repositorio/editar_repo.html',
        #locals(),
        #context_instance=RequestContext(request),
        #)
    
#@login_required
#def detalle_repo(request, nombre_repo, template):
    #repositorio = get_object_or_404(Repositorio, nombre=nombre_repo)
    #repositorios_mios = request.user.repositorios_creados.all()
    #repositorio = Repositorio.objects.filter(creador=request.user)
    #if repositorio:
        #print "hay repo"
    #if repositorio in repositorios_mios:
        #print "hay repo"
    

