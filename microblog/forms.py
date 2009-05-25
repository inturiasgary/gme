#coding: utf-8
from django import forms
from models import Entrada, Conexion
from django.contrib.auth.models import User

class FormEntrada(forms.ModelForm):
    class Meta:
        model  = Entrada
        fields = ('contenido',)
        
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
        
        q = User.objects.filter(username__icontains=nombre) | User.objects.filter(first_name__icontains=nombre) | User.objects.filter(last_name__icontains=nombre) | User.objects.filter(email=email)
        username_exacto = q.filter(username__iexact=nombre)
        
        if username_exacto.count() == 1:
            return username_exacto
        
        return q.distinct()