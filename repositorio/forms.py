from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from repositorio.models import Repositorio
from django import forms
import re

class RegistracionRepo(forms.Form):
    nombre       = forms.CharField(label=_("Nombre Repositorio"), max_length=100, required=True)
    descripcion  = forms.CharField(label=_("Descripcion"), max_length=100, required=False)
    direccionWeb = forms.URLField(label=_("Direccion Web"), required=False)
    emailAdmin   = forms.EmailField(label=_("Email de Aministrador"), required=False)
    
    def clean_nombre(self):
        nombre = self.changed_data["nombre"]
        if not re.search(r'^\w+$', nombre):
            raise forms.ValidationError(_('Nombre de repositorio solo puede contener caracteres.'))
        try:
            Repositorio.objects.get(nombre=nombre)
        except ObjectDoesNotExist:
            return nombre
        raise forms.ValidationError(_('Nombre de repositorio ya registrado, favor elige otro.'))
            
            
    