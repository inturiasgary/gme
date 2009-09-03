from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from repositorio.models import Repositorio
from todo.models import Item, List

class AddListForm(ModelForm):
    # slug = models.SlugField(widget=HiddenInput)
    # slug = forms.CharField(widget=forms.HiddenInput) 
    
    def __init__(self, user, *args, **kwargs):
        super(AddListForm, self).__init__(*args, **kwargs)
        #self.fields['group'].queryset = Group.objects.filter(user=user)
	#Aun no condicionamos que sea un repositorio activo
	self.fields['grupo'].queryset = Repositorio.objects.filter(miembros=user, miembro__creador=True, miembro__activo=True)

    class Meta:
        model = List
        
class AddItemForm(ModelForm):
    due_date = forms.DateField(
                    required=False,
                    widget=forms.DateTimeInput(attrs={'class':'due_date_picker'})
                    )
                    
    title = forms.CharField(
                    widget=forms.widgets.TextInput(attrs={'size':35})
                    ) 

    def __init__(self, task_list, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        # print dir(self.fields['list'])
        # print self.fields['list'].initial
        # self.fields['assigned_to'].queryset = User.objects.filter(groups__in=[task_list.group])
        repositorio = Repositorio.objects.filter(nombre=task_list.grupo.nombre)
	print repositorio
	self.fields['assigned_to'].queryset = User.objects.filter(repositorio=repositorio)

    class Meta:
        model = Item
	
class extendido(ModelForm):
    def __init__(self, user=None, repo_id = None, *args, **kwargs):
        self.user = user
	self.repo_id = repo_id
        super(extendido, self).__init__(*args, **kwargs)
        
class EditItemForm(ModelForm):
    
    #self.fields['assigned_to'].queryset = User.objects.filter(repositorio__id=repo_id)
    
    class Meta:
        model = Item
	fields = ('title','list','due_date','completed','assigned_to', 'note')