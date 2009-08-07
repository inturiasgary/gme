from django.db import models
from django.forms.models import ModelForm
from django import forms
from repositorio.models import Repositorio
from django.contrib import admin
from django.contrib.auth.models import User
import string, datetime

class List(models.Model):
    name        = models.CharField(max_length=60)
    slug        = models.SlugField(max_length=60,editable=False)
    grupo       = models.ForeignKey(Repositorio)
    
    def save(self):
        if not self.id:
            # Replace spaces in slug with hyphens, and lowercase.
            self.slug = (self.name).lower().replace(' ','-')
            
            # Regex to remove non-alphanumeric chars, using re (regular experession module)
            # If we end up with double hyphens, remove those too.
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
    title = models.CharField(max_length=140)
    list = models.ForeignKey(List)
    created_date = models.DateField()    
    due_date = models.DateField(blank=True,null=True,)
    completed = models.BooleanField()
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    assigned_to = models.ForeignKey(User, related_name='todo_assigned_to')
    note = models.TextField(blank=True)
    priority = models.PositiveIntegerField(max_length=3)
    
    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Retorna True si la fecha actual excede de la fecha esperada."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title
        
    # Auto-set the item creation date
    def save(self):
        # Set datetime on initial item save (better than deprecated auto_now_add)
        if not self.id:
            self.created_date = datetime.datetime.now()
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]        

class Comment(models.Model):    
    """
    Not using Django's built-in comments becase we want to be able to save 
    a comment and change task details at the same time. Rolling our own since it's easy.
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