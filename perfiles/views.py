from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from perfiles.models import Perfil
from perfiles.forms import PerfilForm

try:
    from notification import models as notification
except ImportError:
    notification = None

def perfiles(request, template_name="perfiles/perfiles.html"):
    return render_to_response(template_name, {
        "users": User.objects.all().order_by("-date_joined"),
    }, context_instance=RequestContext(request))

def perfil(request, username, template_name="perfiles/perfil.html"):
    other_user = get_object_or_404(User, username=username)
    email_addresses = other_user.emailaddress_set.all()
    if request.user.is_authenticated():
        # is_friend = Friendship.objects.are_friends(request.user, other_user)
        # other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        is_me = False    
    if is_me:
        if request.method == "POST":
            if request.POST["action"] == "actualizar":
                perfil_form = PerfilForm(request.POST, instance=other_user.get_profile())
                if perfil_form.is_valid():
                    perfil = perfil_form.save(commit=False)
                    perfil.user = other_user
                    perfil.save()
            else:
                perfil_form = PerfilForm(instance=other_user.get_profile())
        else:
            perfil_form = PerfilForm(instance=other_user.get_profile())
    else:
        perfil_form = None

    return render_to_response(template_name, {
        "perfil_form": perfil_form,
        "is_me": is_me,
        "other_user": other_user,
        "email_addresses": email_addresses,
    }, context_instance=RequestContext(request))
