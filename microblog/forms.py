from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

class RegistracionForm(forms.Form):
    ''' Creacion del formulario para la registracion de nuevos usuarios '''
    nombre        = forms.CharField(label=_("Nombre"), max_length=100, required=True)
    apellido      = forms.CharField(label=_("Apellido(s)"), max_length=100, required=False)
    nombreusuario = forms.CharField(label=_("Nombre de usuario"), max_length=30, required=True)
    email         = forms.EmailField(label="Email")
    contrasena1   = forms.CharField(label=_("Contrasena"),
                                    widget=forms.PasswordInput()
                                    )
    contrasena2   = forms.CharField(label=_("Contrasena(escriba de nuevo)"),
                                    widget=forms.PasswordInput()
                                    )
    def clean_contrasena2(self):
        if "contrasena1" in self.cleaned_data:
            contrasena1 = self.cleaned_data["contrasena1"]
            contrasena2 = self.cleaned_data["contrasena2"]
            if contrasena1 == contrasena2:
                return contrasena2
        raise forms.ValidationError(_('Error en las contrasenas.'))
    
    def clean_nombreusuario(self):
        nombreusuario = self.changed_data["nombreusuario"]
        if not re.search(r'^\w+$', nombreusuario):
            raise forms.ValidationError(_('Nombre de usuario solo puede contener caracteres.'))
        try:
            User.objects.get(username=nombreusuario)
        except ObjectDoesNotExist:
            return nombreusuario
        raise forms.ValidationError(_('Nombre de usuario ya registrado, favor elige otro.'))
            