from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from cuenta.forms import RegistroForm, AddEmailForm, LoginForm, ChangePasswordForm, ResetPasswordForm, ChangeTimezoneForm, ChangeLanguageForm
from emailconfirmation.models import EmailAddress, EmailConfirmation

def login(request, form_class=LoginForm, template_name="cuenta/login.html"):
    if request.method == "POST":
        default_redirect_to = getattr(settings, "LOGIN_REDIRECT_URLNAME", None)
        if default_redirect_to:
            default_redirect_to = reverse(default_redirect_to)
        else:
            default_redirect_to = settings.LOGIN_REDIRECT_URL
        redirect_to = request.REQUEST.get("next")
        # para asegurarnos que en el get no hayga basura
        if not redirect_to or "://" in redirect_to or " " in redirect_to:
            redirect_to = default_redirect_to
        form = form_class(request.POST)
        if form.login(request): # creacion del cookie y retorna true en caso que se realize bien la accion de creacion de sesion
            return HttpResponseRedirect(redirect_to)
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

def registro(request, form_class=RegistroForm, template_name="cuenta/registro.html", success_url=None):
    if success_url is None:
        success_url = reverse("what_next")
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            username, password = form.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            request.user.message_set.create(message=_("login succesfully as %(username)s.") % {'username': user.username})
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

def email(request, form_class=AddEmailForm, template_name="cuenta/email.html"):
    if request.method == "POST" and request.user.is_authenticated():
        if request.POST["action"] == "add":
            add_email_form = form_class(request.user, request.POST)
            if add_email_form.is_valid():
                add_email_form.save()
                add_email_form = form_class() # @@@
        else:
            add_email_form = form_class()
            if request.POST["action"] == "send":
                email = request.POST["email"]
                try:
                    email_address = EmailAddress.objects.get(user=request.user, email=email)
                    request.user.message_set.create(message=_("Confirmation email sent to %s") % email)
                    EmailConfirmation.objects.send_confirmation(email_address)
                except EmailAddress.DoesNotExist:
                    pass
            elif request.POST["action"] == "remove":
                email = request.POST["email"]
                try:
                    email_address = EmailAddress.objects.get(user=request.user, email=email)
                    email_address.delete()
                    request.user.message_set.create(message=_("Removed email address %s") % email)
                except EmailAddress.DoesNotExist:
                    pass
            elif request.POST["action"] == "primary":
                email = request.POST["email"]
                email_address = EmailAddress.objects.get(user=request.user, email=email)
                email_address.set_as_primary()
    else:
        add_email_form = form_class()
    return render_to_response(template_name, {
        "add_email_form": add_email_form,
    }, context_instance=RequestContext(request))
email = login_required(email)

def password_change(request, form_class=ChangePasswordForm,
        template_name="cuenta/password_change.html"):
    if request.method == "POST":
        password_change_form = form_class(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            password_change_form = form_class(request.user)
    else:
        password_change_form = form_class(request.user)
    return render_to_response(template_name, {
        "password_change_form": password_change_form,
    }, context_instance=RequestContext(request))
password_change = login_required(password_change)

def password_reset(request, form_class=ResetPasswordForm,
        template_name="cuenta/password_reset.html",
        template_name_done="cuenta/password_reset_done.html"):
    if request.method == "POST":
        password_reset_form = form_class(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.save()
            return render_to_response(template_name_done, {
                "email": email,
            }, context_instance=RequestContext(request))
    else:
        password_reset_form = form_class()
    
    return render_to_response(template_name, {
        "password_reset_form": password_reset_form,
    }, context_instance=RequestContext(request))

def timezone_change(request, form_class=ChangeTimezoneForm,
        template_name="cuenta/timezone_change.html"):
    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class(request.user)
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))
timezone_change = login_required(timezone_change)

def language_change(request, form_class=ChangeLanguageForm,
        template_name="cuenta/language_change.html"):
    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
            next = request.META.get('HTTP_REFERER', None)
            return HttpResponseRedirect(next)
    else:
        form = form_class(request.user)
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))
language_change = login_required(language_change)