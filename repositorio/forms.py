from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from repositorio.models import Repositorio
from django import forms
import re

class extendido(forms.ModelForm):
    def __init__(self, update=None, *args, **kwargs):
        self.update = update
        super(extendido, self).__init__(*args, **kwargs)

class FormRepositorio(extendido):
    
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
            #sino existe
            return nombre
        #si existe
        if self.update==None:
            raise forms.ValidationError(_('Nombre de repositorio ya registrado, favor elige otro.'))
        else:
            return nombre

class RepoSaveForm(forms.ModelForm):
    class Meta:
        model = Repositorio
        fields = ('descripcion','direccionWeb','emailAdmin','activo',)

class SearchForm(forms.Form):
    query = forms.CharField(label=_("Enter a keyword to search for"),
                            widget=forms.TextInput(attrs={'size':32}))
    