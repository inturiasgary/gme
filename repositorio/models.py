from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Repositorio(models.Model):
    
    creador     = models.ForeignKey(User)
    nombre      = models.CharField(max_length=100, required = True)
    descripcion = models.CharField(max_length=100)
    fecha       = models.DateTimeField(default=datetime.now, blank=True)
    miembros    = models.ManyToManyField(User, through="Miembro")
    class Meta:
        ordering = ('-fecha',)
    
    def get_absolute_url(self):
        return "%sdfsdf"
    
    def __unicode__(self):
        return "%s creado por %s"%(self.nombre, self.creador.username)
        
class Miembro(models.Model):
    
    fecha_ingreso   = models.DateTimeField(default=datetime.now)
    usuario         = models.ForeignKey(User)
    repositorio     = models.ForeignKey(Repositorio)
    
    class Meta:
        ordering = ('-fecha_ingreso')
        
    def get_absolute_url(self):
        return "%ssdfgdf"
    
    def __unicode__(self):
        return "%s miembro de %s"%(self.usuario.username, self.repositorio.nombre)
# Create your models here.
