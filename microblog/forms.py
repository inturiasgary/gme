from django import forms
from models import Entrada, Conexion
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class FormEntrada(forms.ModelForm):
    contenido = forms.CharField(
                    widget=forms.widgets.Textarea(attrs={'rows':'2','onKeyUp':"javascript:countChars('counter_number')",'width':"140"})
                    ) 
    class Meta:
        model  = Entrada
        fields = ('contenido',)
    
    #def clean_contenido(self):
        #contenido = self.cleaned_data['contenido']
        #if len(contenido)>140:
            #raise forms.ValidationError(_('Solo puedes escribir hasta 140 caracteres.'))
        #else:
            #return contenido
        
class FormConexion(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput)
    
    class Meta:
        model = Conexion
        fields = ('estado',)
        
class FormEncontrarAmigo(forms.Form):
    nombre = forms.CharField(max_length=35, required=False)
    email  = forms.EmailField(max_length=35, required=False)
        
    def encontrar(self):
        nombre = self.cleaned_data['nombre']
        email  = self.cleaned_data['email']
        
        if nombre and email:
            q = User.objects.filter(username__icontains=nombre) | User.objects.filter(first_name__icontains=nombre) | User.objects.filter(last_name__icontains=nombre) | User.objects.filter(email=email)
            q = q.order_by('username')
        else:
            if nombre:
                q = User.objects.filter(username__icontains=nombre) | User.objects.filter(first_name__icontains=nombre) | User.objects.filter(last_name__icontains=nombre)
                q = q.order_by('username')
            else:
                q = User.objects.filter(email__icontains=email)
        
        username_exacto = q.filter(username__iexact=nombre)
        
        if username_exacto.count() == 1:
            return username_exacto
        
        return q