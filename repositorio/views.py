from repositorio.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from forms import FormRepositorio

@login_required
def index(request):
    repositorios_mios      = Repositorio.objects.filter(miembros=request.user, miembro__creador=True)
    repositorios_participo = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=True)
    repositorios_pendiente = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=False)
        
    return render_to_response("repositorio/index.html",
                           locals(),
                           context_instance=RequestContext(request),
                           )

@login_required
def editar_repositorio(request, repositorio_id=None):
    repositorio = None
        
    if request.POST:
        form = FormRepositorio(request.POST, instance=repositorio)
    
        if form.is_valid():
            repositorio      = form.save(False)
            repositorio.user = request.user
            repositorio.save()
            miembro = Miembro(usuario=request.user,repositorio=repositorio, creador=True, activo=True)
            miembro.save()
            #request.user.message_set.create(message=_("Repositorio creado exitosamente"))
            return HttpResponseRedirect('/repositorio/repo/')
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
        repositorio_form  = FormRepositorio(instance=repositorio)
        miembro           = Miembro.objects.get(usuario=request.user, repositorio=repositorio)
        if (miembro.creador == True and miembro.activo == True):
            estado = "Es creador y esta activo"
            is_me = True
        if (miembro.activo == True and miembro.creador == False ):
            estado = "No es creador y esta activo"
            is_me = False
        if (miembro.activo == False):
            estado = "No esta activo"
            is_me = False
    return render_to_response(
        'repositorio/detalle_repositorio.html',
        locals(),
        context_instance=RequestContext(request),
    )
        
@login_required
def repo_save_page(request, repositorio_name):
    repositorio = get_object_or_404(Repositorio, nombre=repositorio_name) 
    ajax = request.GET.has_key('ajax')
    if request.method == 'POST':
        form = RepoSaveForm(request.POST)
        if form.is_valid():
            repositorio = _repositorio_save(request,repositorio_name, form)
    

def delete_repositorio(request):
    if request.method == 'POST':
        repositorio_id = request.POST['repositorio']
        repo = get_object_or_404(Repositorio, pk=repositorio_id)
        repo.delete()
        request.user.message_set.create(message="Repository was deleted succesfully.")
        repositorios_mios      = Repositorio.objects.filter(miembros=request.user, miembro__creador=True)
        repositorios_participo = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=True)
        repositorios_pendiente = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=False)
        
    return render_to_response("repositorio/index.html",
                           locals(),
                           context_instance=RequestContext(request),
                           )

def edit_repositorio(request):
    if request.method == "POST":
        repositorio_id = request.POST['repositorio']
        repositorio       = get_object_or_404(Repositorio, pk=repositorio_id)
        if request.POST['do']=='edit':
            form = FormRepositorio(instance=repositorio)
            context = RequestContext(request)
            return render_to_response('repositorio/repositorio_edit_form.html',
                                      {'form':form, 'value':'update','repositorio':repositorio.id},
                                      context_instance=context)
        if request.POST['do']=='update':
            form = FormRepositorio(instance=repo, data=request.POST)
            if form.is_valid():
                request.user.message_set.create(message="The repository was update succesfully!.")
                repositorios_mios      = Repositorio.objects.filter(miembros=request.user, miembro__creador=True)
                repositorios_participo = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=True)
                repositorios_pendiente = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=False)
    
        return render_to_response("repositorio/index.html",
                                  locals(),
                                  context_instance=RequestContext(request),
                                  )