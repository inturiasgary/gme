from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from repositorio.models import Repositorio
from django import forms
import re

class FormRepositorio(forms.ModelForm):
    class Meta:
        model = Repositorio
        fields = ('nombre','descripcion','direccionWeb','emailAdmin','activo')
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not re.search(r'^\w+$', nombre):
            raise forms.ValidationError(_('Nombre de repositorio solo puede contener caracteres.'))
        try:
            Repositorio.objects.get(nombre=nombre)
        except ObjectDoesNotExist:
            return nombre
        raise forms.ValidationError(_('Nombre de repositorio ya registrado, favor elige otro.'))

class RepoSaveForm(forms.ModelForm):
    class Meta:
        model = Repositorio
        fields = ('descripcion','direccionWeb','emailAdmin','activo',)
    