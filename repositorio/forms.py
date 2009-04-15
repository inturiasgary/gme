from django.utils.translation import gettext_lazy as _
from django import forms

class RegistracionRepo(forms.Form):
    nombre       = forms.CharField(label=_("Nombre Repositorio"), max_length=100, required=True)
    descripcion  = forms.CharField(label=_("Descripcion"), max_length=100, required=False)
    direccionWeb = forms.URLField(label=_("Direccion Web"), required=False)
    emailAdmin   = forms.EmailField(label=_("Email de Aministrador"), required=False)
    
    