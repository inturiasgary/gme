#coding: utf-8
import re #importacion para el uso de expresiones regulares

from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import smart_unicode

from misc.utils import get_send_mail
send_mail = get_send_mail()

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from emailconfirmation.models import EmailAddress
from cuenta.models import Cuenta

from timezones.forms import TimeZoneField #para hacer el uso de zonas horarias

class LoginForm(forms.Form):

    username      = forms.CharField(label=_("Nombre de usuario"), max_length=30, widget=forms.TextInput())
    password      = forms.CharField(label=_(u"Contraseña"), widget=forms.PasswordInput(render_value=False))
    recordar      = forms.BooleanField(label=_(u"Recordármelo"), help_text=_(u"Si elije la opción, sera recordada por 3 semanas"), required=False)

    user = None

    def clean(self):
        if self._errors:
            return
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("Esta cuenta esta actualmente inactiva."))
        else:
            raise forms.ValidationError(_(u"El nombre usuario y/o contraseña son incorrectos."))
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            request.user.message_set.create(message=ugettext(u"Satisfactoriamente logeado como %(username)s.") % {'username': self.user.username})
            if self.cleaned_data['recordar']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False


alnum_re = re.compile(r'^\w+$')
class RegistroForm(forms.Form):

    nombreUsuario    = forms.CharField(label=_("Nombre de usuario"), max_length=30, widget=forms.TextInput())
    password1        = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password2        = forms.CharField(label=_("Password(de nuevo)"), widget=forms.PasswordInput(render_value=False))
    email            = forms.EmailField(label=_("Email (opcional)"), required=False, widget=forms.TextInput())
    confirmation_key = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())

    def clean_nombreUsuario(self):
        if not alnum_re.search(self.cleaned_data["nombreUsuario"]):
            raise forms.ValidationError(_("Nombre de usuario solo puede contener caracteres, numbers and underscores."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["nombreUsuario"])
        except User.DoesNotExist:
            return self.cleaned_data["nombreUsuario"]
        raise forms.ValidationError(_("Nombre de usuario ya en uso. Escoje otro."))

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("Debes escribir la misma contrasenia."))
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data["nombreUsuario"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        if self.cleaned_data["confirmation_key"]:
            from friends.models import JoinInvitation # @@@ temporary fix for issue 93
            try:
                join_invitation = JoinInvitation.objects.get(confirmation_key = self.cleaned_data["confirmation_key"])
                confirmed = True
            except JoinInvitation.DoesNotExist:
                confirmed = False
        else:
            confirmed = False

        # @@@ clean up some of the repetition below -- DRY!

        if confirmed:
            if email == join_invitation.contact.email:
                new_user = User.objects.create_user(username, email, password)
                join_invitation.accept(new_user) # should go before creation of EmailAddress below
                new_user.message_set.create(message=ugettext(u"Your email address has already been verified"))
                # already verified so can just create
                EmailAddress(user=new_user, email=email, verified=True, primary=True).save()
            else:
                new_user = User.objects.create_user(username, "", password)
                join_invitation.accept(new_user) # should go before creation of EmailAddress below
                if email:
                    new_user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': email})
                    EmailAddress.objects.add_email(new_user, email)
            return username, password # required for authenticate()
        else:
            new_user = User.objects.create_user(username, "", password)
            if email:
                new_user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': email})
                EmailAddress.objects.add_email(new_user, email)
            return username, password # required for authenticate()


class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)

class CuentaForm(UserForm):

    def __init__(self, *args, **kwargs):
        super(CuentaForm, self).__init__(*args, **kwargs)
        try:
            self.cuenta = Cuenta.objects.get(user=self.user)
        except Cuenta.DoesNotExist:
            self.cuenta = Cuenta(user=self.user)


class AddEmailForm(UserForm):

    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'30'}))

    def clean_email(self):
        try:
            EmailAddress.objects.get(user=self.user, email=self.cleaned_data["email"])
        except EmailAddress.DoesNotExist:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_("This email address already associated with this account."))

    def save(self):
        self.user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': self.cleaned_data["email"]})
        return EmailAddress.objects.add_email(self.user, self.cleaned_data["email"])


class ChangePasswordForm(UserForm):

    oldpassword = forms.CharField(label=_(u"Contraseña actual"), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=_(u"Nueva contraseña"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_(u"Nueva Contraseña (nuevamente)"), widget=forms.PasswordInput(render_value=False))

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password2"]

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()
        self.user.message_set.create(message=ugettext(u"Password successfully changed."))


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'30'}))

    def clean_email(self):
        if EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True).count() == 0:
            raise forms.ValidationError(_("Email address not verified for any user account"))
        return self.cleaned_data["email"]

    def save(self):
        for user in User.objects.filter(email__iexact=self.cleaned_data["email"]):
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            subject = _("Password reset")
            message = render_to_string("cuenta/password_reset_message.txt", {
                "user": user,
                "new_password": new_password,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], priority="high")
        return self.cleaned_data["email"]

class ChangeTimezoneForm(CuentaForm):

    timezone = TimeZoneField(label=_("Timezone"), required=True)

    def __init__(self, *args, **kwargs):
        super(ChangeTimezoneForm, self).__init__(*args, **kwargs)
        self.initial.update({"timezone": self.cuenta.timezone})

    def save(self):
        self.cuenta.timezone = self.cleaned_data["timezone"]
        self.cuenta.save()
        self.user.message_set.create(message=ugettext(u"Huso Horario  actualizado."))

class ChangeLanguageForm(CuentaForm):

    language = forms.ChoiceField(label=_("Language"), required=True, choices=settings.LANGUAGES)

    def __init__(self, *args, **kwargs):
        super(ChangeLanguageForm, self).__init__(*args, **kwargs)
        self.initial.update({"language": self.account.language})

    def save(self):
        self.account.language = self.cleaned_data["language"]
        self.account.save()
        self.user.message_set.create(message=ugettext(u"Language successfully updated."))


# @@@ these should somehow be moved out of account or at least out of this module

#from account.models import OtherServiceInfo, other_service, update_other_services

#class TwitterForm(UserForm):
    #username = forms.CharField(label=_("Username"), required=True)
    #password = forms.CharField(label=_("Password"), required=True,
                               #widget=forms.PasswordInput(render_value=False))

    #def __init__(self, *args, **kwargs):
        #super(TwitterForm, self).__init__(*args, **kwargs)
        #self.initial.update({"username": other_service(self.user, "twitter_user")})

    #def save(self):
        #from zwitschern.utils import get_twitter_password
        #update_other_services(self.user,
            #twitter_user = self.cleaned_data['username'],
            #twitter_password = get_twitter_password(settings.SECRET_KEY, self.cleaned_data['password']),
        #)
        #self.user.message_set.create(message=ugettext(u"Successfully authenticated."))