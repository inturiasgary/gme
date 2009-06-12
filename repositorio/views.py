from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import FormRepositorio

def index(request):
    if request.user.is_authenticated():
        repositorios_mios = Repositorio.objects.filter(miembros=request.user, miembro__creador=True)
        repositorios_participo = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=True)
        repositorios_pendiente = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=False)
        
    return render_to_response("repositorio/index.html",
                           locals(),
                           context_instance=RequestContext(request),
                           )

@login_required
def editar_repositorio(request, repositorio_id=None):
    if repositorio_id:
        repositorio   = get_object_or_404(Repositorio, id=repositorio_id)
        editar_nombre = True
    else:
        repositorio = None
        
    if request.POST:
        form = FormRepositorio(request.POST, instance=repositorio)
    
        if form.is_valid():
            repositorio = form.save(False)
            repositorio.user = request.user
            repositorio.save()
            miembro = Miembro(usuario=request.user,repositorio=repositorio, creador=True, activo=True)
            miembro.save()
    else:
        form = FormRepositorio(instance=repositorio)
    return render_to_response(
        'repositorio/editar_repositorio.html',
        locals(),
        context_instance=RequestContext(request),
    )

@login_required
def repo(request, nombre=None):
    if nombre:
        repositorio       = get_object_or_404(Repositorio, nombre=nombre)
        miembro           = Miembro.objects.get(usuario=request.user, repositorio=repositorio)
        if (miembro.creador == True and miembro.activo == True):
            estado = "Es creador y esta activo"
        if (miembro.activo == True ):
            estado = "No es creador y esta activo"
        if (miembro.activo == False):
            estado = "No esta activo"
    return render_to_response(
        'repositorio/detalle_repositorio.html',
        locals(),
        context_instance=RequestContext(request),
    )
        

