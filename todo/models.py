from django.db import models
from django.forms.models import ModelForm
from django import forms
from repositorio.models import Repositorio
from django.contrib import admin
from django.contrib.auth.models import User
import string, datetime
from django.utils.translation import get_language_from_request
from django.utils.translation import ugettext_lazy as _

class List(models.Model):
    name        = models.CharField(max_length=60, verbose_name=_("Name"))
    slug        = models.SlugField(max_length=60, editable=False)
    grupo       = models.ForeignKey(Repositorio)
    
    def save(self):
        if not self.id:
            # remplazo de los espacios por guiones
            self.slug = (self.name).lower().replace(' ','-')
            
            # para remover caracteres no alfanumericos, usando re (modulo de expresiones regulares)
            # si termina con doble guien, corta.
            import re
            self.slug = re.sub(r"[^A-Za-z0-9\-]", "", self.slug).replace('--','-')

            super(List, self).save()

    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ["name"]        
        verbose_name_plural = "Lists"
        
        # Prevee que se creen en un repositorio dos listas o mas con el mismo nombre
        unique_together = ("grupo", "slug")
        
class Item(models.Model):
    title = models.CharField(max_length=140, verbose_name=_("Title"))
    list = models.ForeignKey(List, verbose_name=_("List"))
    created_date = models.DateField()    
    due_date = models.DateField(blank=True,null=True,verbose_name=_("Due date"))
    completed = models.BooleanField(verbose_name=("Completed"))
    completed_date = models.DateField(blank=True,null=True,verbose_name=_("Completed date"))
    created_by = models.ForeignKey(User, related_name='created_by', verbose_name=_("Created by"))
    assigned_to = models.ForeignKey(User, related_name='todo_assigned_to', verbose_name=_("Todo asigned to"))
    note = models.TextField(blank=True)
    priority = models.PositiveIntegerField(max_length=3)
    
    def overdue_status(self):
        "Retorna True si la fecha actual excede de la fecha esperada."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title
        
    # fecha de completado automaticamente.
    def save(self):
        if not self.id:
            self.created_date = datetime.datetime.now()
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]        

class Comment(models.Model):    
    """
    No se usa la aplicacion interna de django para hablitar el save de un cometario
    y cambiar los detalles de tareas al mismo tiempo.
    """
    author = models.ForeignKey(User)
    task = models.ForeignKey(Item)
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=True)
    
    def __unicode__(self):        
        return '%s - %s' % (
                self.author, 
                self.date, 
                )        