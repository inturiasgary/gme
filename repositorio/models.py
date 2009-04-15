from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Repositorio(models.Model):
    
    creador     = models.ForeignKey(User, related_name="repositorios_creados", verbose_name=_("creador"))
    nombre      = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)
    fecha       = models.DateTimeField(default=datetime.now, blank=True)
    miembros    = models.ManyToManyField(User, through="Miembro")
    borrado     = models.BooleanField(_("borrado"), default=False)
    
    #class Meta:
        #ordering = ('-fecha',)
    
    def get_absolute_url(self):
        return "%sdfsdf"
    
    def __unicode__(self):
        return "%s creado por %s"%(self.nombre, self.creador.username)
        
class Miembro(models.Model):
    
    fecha_ingreso   = models.DateTimeField(default=datetime.now)
    usuario         = models.ForeignKey(User)
    repositorio     = models.ForeignKey(Repositorio)
    bloqueado       = models.BooleanField(_("bloqueado"), default=False) #El creador del repositorio decidira a quien bloquear
    
    #class Meta:
        #ordering = ('-fecha_ingreso')
        
    def get_absolute_url(self):
        return "%ssdfgdf"
    
    def __unicode__(self):
        return "%s miembro de %s"%(self.usuario.username, self.repositorio.nombre)
# Create your models here.

class Topico(models.Model):
    '''discussion hacerca del repositorio'''
    repositorio = models.ForeignKey(Repositorio)
    titulo      = models.CharField(_("titulo"), max_length=50)
    creador     = models.ForeignKey(User, related_name="topicos_creados", verbose_name=_("creador"))
    modificado  = models.DateTimeField(_("modificado"), default=datetime.now)
    cuerpo      = models.TextField(_('cuerpo'), blank=True)
    
    def __unicode__(self):
        return self.titulo
    #class Meta:
        #ordering = ("-modificado")
        
class Commit(models.Model):
    usuario     = models.ForeignKey(User)
    repositorio = models.ForeignKey(Repositorio)
    fecha       = models.DateTimeField(default=datetime.now)
    descripcion = models.CharField(max_length=100)
    recipientes = models.ManyToManyField(User, related_name='commits_recibidos')
    
    def __unicode__(self):
        return "%s en %s"%(self.usuario.username, self.repositorio.nombre)
    def get_absolute_url(self):
        return "asdfsadf"
    