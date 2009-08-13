from django import forms 
from django.shortcuts import render_to_response
from todo.models import Item, List, Comment
from todo.forms import AddListForm, AddItemForm, EditItemForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
import datetime

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
    # Only show lists to the user that belong to groups they are members of.
    # Staff users see all lists
    if request.user.is_staff:
        list_list = List.objects.all().order_by('name')
    else:
        list_list = List.objects.filter(grupo__in=request.user.repositorio_set.filter(miembro__activo=True)).order_by('name')

    # Count everything
    list_count = list_list.count()

    # Note admin users see all lists, so count shouldn't filter by just lists the admin belongs to
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
def del_list(request,list_id,list_slug):

    """
    Delete an entire list. Danger Will Robinson! Only staff members should be allowed to access this view.
    """

    if request.user.is_staff:
        can_del = 1

    # Get this list's object (to derive list.name, list.id, etc.)
    list = get_object_or_404(List, slug=list_slug)

    # If delete confirmation is in the POST, delete all items in the list, then kill the list itself
    if request.method == 'POST':
        # Can the items
        del_items = Item.objects.filter(list=list.id)
        for del_item in del_items:
            del_item.delete()

        # Kill the list
        del_list = List.objects.get(id=list.id)
        del_list.delete()

        # A var to send to the template so we can show the right thing
        list_killed = 1

    else:
        item_count_done = Item.objects.filter(list=list.id,completed=1).count()
        item_count_undone = Item.objects.filter(list=list.id,completed=0).count()
        item_count_total = Item.objects.filter(list=list.id).count()    

    return render_to_response('todo/del_list.html', locals(), context_instance=RequestContext(request))


@login_required
def view_list(request,list_id=0,list_slug='',view_completed=0):

    """
    Display and manage items in a task list
    """

    # Make sure the accessing user has permission to view this list.
    # Always authorize the "mine" view. Admins can view/edit all lists.

    if list_slug == "mine" :
        auth_ok =1
    else: 
        list = get_object_or_404(List, slug=list_slug)
        listid = list.id    

        # Check whether current user is a member of the group this list belongs to.
        if list.grupo in request.user.repositorio_set.all() or request.user.is_staff or list_slug == "mine" :
            auth_ok = 1   # User is authorized for this view
        else: # User does not belong to the group this list is attached to
            request.user.message_set.create(message=_("You do not have permission to view/edit this list."))


    # First check for items in the mark_done POST array. If present, change
    # their status to complete.
    if request.POST.getlist('mark_done'):
        done_items = request.POST.getlist('mark_done')
        # Iterate through array of done items and update its representation in the model
        for thisitem in done_items:
            p = Item.objects.get(id=thisitem)
            p.completed = 1
            p.completed_date = datetime.datetime.now()
            p.save()
            request.user.message_set.create(message=_("Item \"%s\" marked complete.") % p.title )


        # Undo: Set completed items back to incomplete
    if request.POST.getlist('undo_completed_task'):
        undone_items = request.POST.getlist('undo_completed_task')
        for thisitem in undone_items:
            p = Item.objects.get(id=thisitem)
            p.completed = 0
            p.save()
            request.user.message_set.create(message=_("Previously completed task \"%s\" marked incomplete.") % p.title)	        


    # And delete any requested items
    if request.POST.getlist('del_task'):
        deleted_items = request.POST.getlist('del_task')
        for thisitem in deleted_items:
            p = Item.objects.get(id=thisitem)
            p.delete()
            request.user.message_set.create(message=_("Item \"%s\" deleted.") % p.title )

    # And delete any *already completed* items
    if request.POST.getlist('del_completed_task'):
        deleted_items = request.POST.getlist('del_completed_task')
        for thisitem in deleted_items:
            p = Item.objects.get(id=thisitem)
            p.delete()
            request.user.message_set.create(message=_("Deleted previously completed item \"%s\".")  % p.title)


    thedate = datetime.datetime.now()
    created_date = "%s-%s-%s" % (thedate.year, thedate.month, thedate.day)


    # Get list of items with this list ID, or filter on items assigned to me
    if list_slug == "mine":
        task_list = Item.objects.filter(assigned_to=request.user, completed=0)
        completed_list = Item.objects.filter(assigned_to=request.user, completed=1)
    else:
        task_list = Item.objects.filter(list=list.id, completed=0)
        completed_list = Item.objects.filter(list=list.id, completed=1)


    if request.POST.getlist('add_task') :
        form = AddItemForm(list, request.POST,initial={
            'assigned_to':request.user.id,
            'priority':999,
        })

        if form.is_valid():
            # Save task first so we have a db object to play with
            new_task = form.save()

            # Send email alert only if the Notify checkbox is checked AND the assignee is not the same as the submittor
            # Email subect and body format are handled by templates
            if "notify" in request.POST :
                if new_task.assigned_to != request.user :
                    current_site = Site.objects.get_current() # Need this for link in email template

                    # Send email
                    email_subject = render_to_string("todo/email/assigned_subject.txt", { 'task': new_task })                    
                    email_body = render_to_string("todo/email/assigned_body.txt", { 'task': new_task, 'site': current_site, })
                    try:
                        send_mail(email_subject, email_body, new_task.created_by.email, [new_task.assigned_to.email], fail_silently=False)
                    except:
                        request.user.message_set.create(message=_("Task saved but mail not sent. Contact your administrator.") )

            request.user.message_set.create(message=_("New task \"%s\" has been added.") % new_task.title )
            return HttpResponseRedirect(request.path)

    else:
        if list_slug != "mine" : # We don't allow adding a task on the "mine" view
            form = AddItemForm(list, initial={
                'assigned_to':request.user.id,
                'priority':999,
            } )

    if request.user.is_staff:
        can_del = 1

    return render_to_response('todo/view_list.html', locals(), context_instance=RequestContext(request))


@login_required
def view_task(request,task_id):

    """
    View task details. Allow task details to be edited.
    """

    task = get_object_or_404(Item, pk=task_id)
    comment_list = Comment.objects.filter(task=task_id)

    # Before doing anything, make sure the accessing user has permission to view this item.
    # Determine the group this task belongs to, and check whether current user is a member of that group.
    # Admins can edit all tasks.

    if task.list.grupo in request.user.repositorio_set.all() or request.user.is_staff:

        auth_ok = 1
        # Distinguish between POSTs from the two forms on the page (edit task and add comment) by detecting a field name
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
                return HttpResponseRedirect(reverse('todo-incomplete_tasks', args=[task.list.id, task.list.slug]))

        else:
            form = EditItemForm(instance=task)
            thedate = task.due_date
    else:
        request.user.message_set.create(message=_("You do not have permission to view/edit this task."))

    return render_to_response('todo/view_task.html', locals(), context_instance=RequestContext(request))



# @login_required
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


