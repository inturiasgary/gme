from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

#from friends.forms import InviteFriendForm
#from friends.models import FriendshipInvitation, Friendship

from perfiles.models import Perfil
from perfiles.forms import PerfilForm

# # used by friend autocompletion
# from gravatar.templatetags.gravatar import gravatar

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
    if request.user.is_authenticated():
        # is_friend = Friendship.objects.are_friends(request.user, other_user)
        # other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        # other_friends = []
        # is_friend = False
        is_me = False
    
#   if is_friend:
#       invite_form = None
#       previous_invitations_to = None
#       previous_invitations_from = None
#    else:
#        if request.user.is_authenticated() and request.method == "POST":
#            if request.POST["action"] == "invite":
#                invite_form = InviteFriendForm(request.user, request.POST)
#                if invite_form.is_valid():
#                    invite_form.save()
#            else:
#                invite_form = InviteFriendForm(request.user, {
#                    'to_user': username,
#                    'message': ugettext("Let's be friends!"),
#                })
#                if request.POST["action"] == "accept": # @@@ perhaps the form should just post to friends and be redirected here
#                    invitation_id = request.POST["invitation"]
#                    try:
#                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
#                        if invitation.to_user == request.user:
#                            invitation.accept()
#                            request.user.message_set.create(message=_("You have accepted the friendship request from %(from_user)s") % {'from_user': invitation.from_user})
#                            is_friend = True
#                            other_friends = Friendship.objects.friends_for_user(other_user)
#                    except FriendshipInvitation.DoesNotExist:
#                        pass
#        else:
#            invite_form = InviteFriendForm(request.user, {
#                'to_user': username,
#                'message': ugettext("Let's be friends!"),
#            })
#    previous_invitations_to = FriendshipInvitation.objects.filter(to_user=other_user, from_user=request.user)
#    previous_invitations_from = FriendshipInvitation.objects.filter(to_user=request.user, from_user=other_user)
    
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
#        "is_friend": is_friend,
        "other_user": other_user,
#        "other_friends": other_friends,
#        "invite_form": invite_form,
#        "previous_invitations_to": previous_invitations_to,
#        "previous_invitations_from": previous_invitations_from,
    }, context_instance=RequestContext(request))
