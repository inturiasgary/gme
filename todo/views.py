from django import forms 
from django.shortcuts import render_to_response, get_object_or_404
from todo.models import Item, List, Comment
from todo.forms import AddListForm, AddItemForm, EditItemForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.translation import ugettext as _
import datetime

from repositorio.models import Miembro, Repositorio, Mensaje

@login_required
def list_lists(request):

    """
    vista principal - muestra la lista y se pueden adicionar.
    """
    # El concepto de repositorios es lo mismo que grupos.
    group_count = request.user.repositorio_set.filter(miembro__activo=True).count()
    if group_count == 0:
        request.user.message_set.create(message=_("You don't appear belong to any repository. Enter at least to one."))

    # Muestra la lista de repositorios donde el usuario es miembro
    # Solo muestra la lista de usuarios que son miembros del repositorio.
    # el administrador puede ver todos los usuarios
    if request.user.is_staff:
        list_list = List.objects.all().order_by('name')
    else:
        list_list = List.objects.filter(grupo__in=request.user.repositorio_set.filter(miembro__activo=True)).order_by('name')

    # Cuenta todos
    list_count = list_list.count()

    # el administrador puede ver todas las listas
    if request.user.is_staff :
        item_count = Item.objects.filter(completed=0).count()        
    else:
        item_count = Item.objects.filter(completed=0).filter(list__grupo__in=request.user.repositorio_set.filter(miembro__activo=True)).count()


    if request.POST:    
        form = AddListForm(request.user,request.POST)
        if form.is_valid():
            try:
                form.save()
                request.user.message_set.create(message=_("A new list has been created."))
                return HttpResponseRedirect(request.path)
            except IntegrityError:
                request.user.message_set.create(message=_("There was a problem saving the new list. Most likely a list with the same name in the same group already exists."))

    else:
        form = AddListForm(request.user)
        
    return render_to_response('todo/list_lists.html', locals(), context_instance=RequestContext(request))  

@login_required
def del_list(request,repo_id, list_id,list_slug): #aumentado repo id

    """
    Elmina una lista.
    """
    list = get_object_or_404(List, id=list_id)
    if list.grupo in Repositorio.objects.filter(miembros=request.user, miembro__creador=True, miembro__activo=True):

        can_del = 1

    list = get_object_or_404(List, slug=list_slug)

    # Si la confirmacion se da, se elimina todos los items de la lista y la lista
    if request.method == 'POST':
        del_items = Item.objects.filter(list=list.id)
        for del_item in del_items:
            del_item.delete()

        # elimina la lista
        del_list = List.objects.get(id=list.id)
        del_list.delete()

        # cantidad de listas eliminadas
        list_killed = 1

    else:
        item_count_done = Item.objects.filter(list=list.id,completed=1).count()
        item_count_undone = Item.objects.filter(list=list.id,completed=0).count()
        item_count_total = Item.objects.filter(list=list.id).count()    

    return render_to_response('todo/del_list.html', locals(), context_instance=RequestContext(request))


@login_required
def view_list(request,repo_id=0, list_id=0,list_slug='',view_completed=0):

    """
    Muestra y administra los items de una lista
    """
    repositorio = get_object_or_404(Repositorio, id=repo_id)
    # Para verificar la seguridad de ingreso a una lista.
    if list_slug == "mine" :
        
        auth_ok =1
        if repositorio in Repositorio.objects.filter(miembros=request.user, miembro__creador=True, miembro__activo=True):
            can_del = 1
    else: 
        list = get_object_or_404(List, slug=list_slug)
        listid = list.id    

        # verifica si el usuario actual es miembro del repositorio
        if list.grupo in request.user.repositorio_set.all() or request.user.is_staff:
            auth_ok = 1   # El usuario es autorizado para el ingreso a  la lista
            if list.grupo in Repositorio.objects.filter(miembros=request.user, miembro__creador=True, miembro__activo=True):
                can_del = 1
        else: # no se autoriza su ingreso
            request.user.message_set.create(message=_("You do not have permission to view/edit this list."))
        

    if request.POST.getlist('mark_done'):
        done_items = request.POST.getlist('mark_done')
        # Iteracion a traves del arreglo de utems realizados y actualiza en el modelo
        for thisitem in done_items:
            p = Item.objects.get(id=thisitem)
            p.completed = 1
            p.completed_date = datetime.datetime.now()
            p.save()
            request.user.message_set.create(message=_("Item \"%s\" marked complete.") % p.title )


        # establece de nuevo como item no realizado
    if request.POST.getlist('undo_completed_task'):
        undone_items = request.POST.getlist('undo_completed_task')
        for thisitem in undone_items:
            p = Item.objects.get(id=thisitem)
            p.completed = 0
            p.save()
            request.user.message_set.create(message=_("Previously completed task \"%s\" marked incomplete.") % p.title)	        


    # elimina cualquier item
    if request.POST.getlist('del_task'):
        deleted_items = request.POST.getlist('del_task')
        for thisitem in deleted_items:
            p = Item.objects.get(id=thisitem)
            p.delete()
            request.user.message_set.create(message=_("Item \"%s\" deleted.") % p.title )

    # elimina items completados
    if request.POST.getlist('del_completed_task'):
        deleted_items = request.POST.getlist('del_completed_task')
        for thisitem in deleted_items:
            p = Item.objects.get(id=thisitem)
            p.delete()
            request.user.message_set.create(message=_("Deleted previously completed item \"%s\".")  % p.title)


    thedate = datetime.datetime.now()
    created_date = "%s-%s-%s" % (thedate.year, thedate.month, thedate.day)


    # Obtiene la lista de items de la lista dado el ID, filtra los items asignados al usuario
    if list_slug == "mine":
        task_list = Item.objects.filter(assigned_to=request.user, completed=0, list__grupo__id = repo_id )
        completed_list = Item.objects.filter(assigned_to=request.user, completed=1, list__grupo__id = repo_id )
    else:
        usuario_actual = request.user.username
        task_list = Item.objects.filter(list=list.id, completed=0, list__grupo__id = repo_id )
        completed_list = Item.objects.filter(list=list.id, completed=1, list__grupo__id = repo_id)


    if request.POST.getlist('add_task') :
        form = AddItemForm(list, request.POST,initial={
            'assigned_to':request.user.id,
            'priority':999,
        })

        if form.is_valid():
            # primero se graba la tarea para luego editarla
            new_task = form.save()
            commit = Mensaje.objects.create(usuario=new_task.assigned_to , repositorio=repositorio, descripcion='Nueva Tarea: %s - %s'%(new_task.title, new_task.note))

            # Envio de email alerta solo si el checkbos es seleccionado y el asignado no es el mismo que el que esta creando        
            if "notify" in request.POST :
                if new_task.assigned_to != request.user :
                    current_site = Site.objects.get_current() # Necesario para acoplamiento de la plantilla en el email

                    # enviar email
                    email_subject = render_to_string("todo/email/assigned_subject.txt", { 'task': new_task })                    
                    email_body = render_to_string("todo/email/assigned_body.txt", { 'task': new_task, 'site': current_site, })
                    try:
                        send_mail(email_subject, email_body, new_task.created_by.email, [new_task.assigned_to.email], fail_silently=False)
                    except:
                        request.user.message_set.create(message=_("Task saved but mail not sent. Contact your administrator.") )

            request.user.message_set.create(message=_("New task \"%s\" has been added.") % new_task.title )
            return HttpResponseRedirect(request.path)

    else:
        if list_slug != "mine" : # No permitimos el agregar de una tarea en la vista mia
            form = AddItemForm(list, initial={
                'assigned_to':request.user.id,
                'priority':999,
            } )

    #solo adicionado el try
    #try:
        #Controlamos que el usario sea el administrador del repositorio, caso contrario no podra borrar la tarea
        #miembro_creador   = Miembro.objects.get(repositorio__nombre="repositorioUsuario2", usuario__username=request.user.username,creador=True)
        #list_slug = "mine"
    #except:
        #list_slug = "notmine"
    return render_to_response('todo/view_list.html', locals(), context_instance=RequestContext(request))


@login_required
def view_task(request,task_id):

    """
    vista para detalles de tareas. Permite la edicion de las tareas.
    """

    task = get_object_or_404(Item, pk=task_id)
    comment_list = Comment.objects.filter(task=task_id)

    # antes de adicionar cualquier cosa, hace seguro el acceso a usuario con permiso para ver estos items.
    # determina el repositorio al que pertenece esta tarea, verfica si el usuario actual es miembro del repositorio.
    if task.list.grupo in request.user.repositorio_set.all() or request.user.is_staff:
        if task.list.grupo in Repositorio.objects.filter(miembros=request.user, miembro__creador=True, miembro__activo=True):
            can_del = 1

        auth_ok = 1
        if request.POST:
            form = EditItemForm(request.POST,instance=task)
            if form.is_valid():
                form.save()

                    # Also save submitted comment, if non-empty
                if request.POST['comment-body']:
                    c = Comment(
                        author=request.user, 
                        task=task,
                        body=request.POST['comment-body'],
                    )
                    c.save()

                request.user.message_set.create(message=_("The task has been edited."))
                return HttpResponseRedirect(reverse('todo-incomplete_tasks', args=[task.list.grupo.id, task.list.id, task.list.slug]))

        else:
            form = EditItemForm(instance=task)
            thedate = task.due_date
    else:
        request.user.message_set.create(message=_("You do not have permission to view/edit this task."))

    return render_to_response('todo/view_task.html', locals(), context_instance=RequestContext(request))



@login_required
def reorder_tasks(request):
    """
    Handle task re-ordering (priorities) from JQuery drag/drop in view_list.html
    """

    newtasklist = request.POST.getlist('tasktable[]')
    # First item in received list is always empty - remove it
    del newtasklist[0]

    # Items arrive in order, so all we need to do is increment up from one, saving
    # "i" as the new priority for the current object.
    i = 1
    for t in newtasklist:
        newitem = Item.objects.get(pk=t)
        newitem.priority = i
        newitem.save()
        i = i + 1

    # All views must return an httpresponse of some kind ... without this we get 
    # error 500s in the log even though things look peachy in the browser.    
    return HttpResponse(status=201)


