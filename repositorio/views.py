from repositorio.models import Repositorio, Miembro, Mensaje
from django.db.models import Count
import app_settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import FormRepositorio, SearchForm
from models import Miembro

@login_required
def index(request):
    REPOSITORY_URL_BASE     = app_settings.REPOSITORY_URL_BASE
    form_buscar             = SearchForm()
    repositorios_mios       = Repositorio.objects.filter(miembros=request.user, miembro__creador=True)
    repositorios_participo  = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=True)
    repositorios_pendiente  = Repositorio.objects.filter(miembros=request.user, miembro__creador=False, miembro__activo=False)
    return render_to_response("repositorio/index.html",
                           locals(),
                           context_instance=RequestContext(request),
                           )

@login_required
def editar_repositorio(request):
    
    if request.POST:
        form = FormRepositorio(data=request.POST)
    
        if form.is_valid():
            repositorio      = form.save(False)
            repositorio.user = request.user
            repositorio.save()
            miembro = Miembro(usuario=request.user,repositorio=repositorio, creador=True, activo=True)
            miembro.save()
            #request.user.message_set.create(message=_("Repositorio creado exitosamente"))
            return HttpResponseRedirect('/repositorio/repo/')
        else:
            #form = FormRepositorio(data=request.POST)
            context = RequestContext(request)
            return render_to_response('repositorio/editar_repositorio.html',
                                    locals(),
                                    context_instance=context)
    else:
        form = FormRepositorio()
    return render_to_response(
        'repositorio/editar_repositorio.html',
        locals(),
        context_instance=RequestContext(request),
    )

@login_required
def repo(request, nombre=None):
    REPOSITORY_ENTRIES_LIMIT = app_settings.REPOSITORY_ENTRIES_LIMIT
    if nombre:
        repositorio       = get_object_or_404(Repositorio, nombre=nombre)
        miembro_creador   = Miembro.objects.get(repositorio=repositorio, creador=True)
        repositorio_form  = FormRepositorio(instance=repositorio)
        try:
            miembro       = Miembro.objects.get(usuario=request.user, repositorio=repositorio)
        except:
            is_me = False
            miembro_activo = False
        else:
            commits = Mensaje.objects.order_by('-fecha').filter(repositorio=repositorio)[:REPOSITORY_ENTRIES_LIMIT]
            if (miembro.creador == True and miembro.activo == True):
                estado = "Es creador y esta activo"
                is_me = True
                miembro_activo = True
            if (miembro.activo == True and miembro.creador == False ):
                estado = "No es creador y esta activo"
                is_me = False
                miembro_activo = True
            if (miembro.activo == False):
                estado = "No esta activo"
                is_me = False
                miembro_activo = "peticion"
            
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
        return HttpResponseRedirect('/repositorio/repo/')

        
    return render_to_response("repositorio/index.html",
                           locals(),
                           context_instance=RequestContext(request),
                           )

def edit_repositorio(request):
    
    if request.POST.getlist('del_miembro'):
        deleted_items = request.POST.getlist('del_miembro')
        repositorio_nombre = request.POST['repositorio_nombre']
        for thisitem in deleted_items:
            p = Miembro.objects.get(id=thisitem)
            p.delete()
            request.user.message_set.create(message="Borrado la participacion de \"%s\"."  % p.usuario.username)
        return HttpResponseRedirect('/repositorio/detalle/%s/miembros/'%repositorio_nombre)
            
    if request.POST.getlist('add_miembro'):
        deleted_items = request.POST.getlist('add_miembro')
        repositorio_nombre = request.POST['repositorio_nombre']
        for thisitem in deleted_items:
            p = Miembro.objects.get(id=thisitem)
            p.activo = 1
            p.save()
            request.user.message_set.create(message="adicionada la participacion de \"%s\"."  % p.usuario.username)
        return HttpResponseRedirect('/repositorio/detalle/%s/miembros/'%repositorio_nombre)

    if request.POST.get('repositorio'):
        repositorio_id = request.POST['repositorio']
        print "entro aqui en edit_repositorio"
        repo           = get_object_or_404(Repositorio, pk=repositorio_id)
        if request.POST['do']=='edit':
            form = FormRepositorio(instance=repo, update=None)
            context = RequestContext(request)
            return render_to_response('repositorio/repositorio_edit_form.html',
                                      {'form':form, 'value':'update','repositorio':repo.id},
                                      context_instance=context)
        if request.POST['do']=='update':
            form = FormRepositorio(instance=repo, data=request.POST, update=True)
            if form.is_valid():
                form.save()
                request.user.message_set.create(message="The repository was update succesfully!.")
                return HttpResponseRedirect('/repositorio/repo/')
            else:
                context = RequestContext(request)
                return render_to_response('repositorio/repositorio_edit_form.html',
                                          {'form':form, 'value':'update', 'repositorio':repo.id},
                                          context_instance=context)
            
        if request.POST['do']=='activarme':
            miembro, creado = Miembro.objects.get_or_create(usuario=request.user, repositorio=repo)
            if creado == True:
                request.user.message_set.create(message="Se realizo correctamente la peticion al repositorio!.")
            else:
                request.user.message_set.create(message="Peticion ya realizada!.")
            return HttpResponseRedirect('/repositorio/repo/')
        
        if request.POST['do']=='eliminar participacion':
            try:
                miembro = Miembro.objects.get(usuario=request.user, repositorio=repo)
                miembro.delete()
                request.user.message_set.create(message="Eliminada la participacion del repositorio.")
            except:
                request.user.message_set.create(message="Usted no tiene participacion en el repositorio")
            return HttpResponseRedirect('/repositorio/repo/')
        return render_to_response("repositorio/index.html",
                                  locals(),
                                  context_instance=RequestContext(request),
                                  )
    try:
        repositorio_nombre = request.POST['repositorio_nombre']
        return HttpResponseRedirect('/repositorio/detalle/%s/miembros/'%repositorio_nombre)
    except:
        pass
                
def search_repositorio(request): #Trabaja con ajax
    REPOSITORY_URL_BASE = app_settings.REPOSITORY_URL_BASE
    form_buscar = SearchForm()
    repositorios_encontrados = []
    
    if request.GET.has_key('query'):
        mostrar_resultados = True
        query = request.GET['query'].strip() #para poder quitar los espacios
        if query:
            form_buscar              = SearchForm({'query':query})
            repositorios_encontrados = Repositorio.objects.filter(nombre__icontains=query)[:10] #Filtracion solo de los 10 repositorios que tienen similar nombre
    variables = RequestContext(request, {'form_buscar':form_buscar,
                                        'repositorios_encontrados':repositorios_encontrados,
                                        'show_tags':True,
                                        'mostrar_resultados':mostrar_resultados,
                                        'REPOSITORY_URL_BASE':REPOSITORY_URL_BASE,
                                        'show_creador':True})
    if request.GET.has_key('ajax'):
        return render_to_response('repositorio/repositorios_encontrados.html', variables)
    else:
        return render_to_response('repositorio/search.html',variables)
    
def repo_miembros(request, repositorio_nombre):
    repositorio_nombre = repositorio_nombre
    miembros = Miembro.objects.filter(repositorio__nombre=repositorio_nombre) 
    try:
        miembro_creador = Miembro.objects.get(usuario=request.user, repositorio__nombre=repositorio_nombre)
        if miembro_creador.creador == True:
            is_me = True
        else:
            is_me = False
    except:
        is_me = False
    return render_to_response('repositorio/miembros_list.html',
                              locals(),
                              context_instance = RequestContext(request),
                              )    
