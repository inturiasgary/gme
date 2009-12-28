from datetime import datetime
from django.db import models
import app_settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

MENSAJE_REPOSITORIO = 'r' 
MENSAJE_COMMIT      = 'c'
MENSAJE_SIMPLE      = 's'

MENSAJE_CHOICES=(
    (MENSAJE_REPOSITORIO,_('Repositorio')),
    (MENSAJE_COMMIT,_('Commit')),
    (MENSAJE_SIMPLE,_('Simple')),
)

class DefaultRepositorioManager(models.Manager):
    def get_query_set(self):
        return super(DefaultRepositorioManager, self).get_query_set()

class RepositorioManager(models.Manager):
    ''' Fucnion para facilitar el conteo de usuario activos y pendientes en cada repositorio'''
    def get_query_set(self):
        return super(RepositorioManager, self).get_query_set()
    def numero_miembros_activo(self):
        result = self.get_query_set().values('nombre').annotate(miembros_activos=Count('pk')).filter(miembro__activo=True)
        return result.annotate(miembros_pendientes=Count('pk')).filter(miembro__activo=False)
    def numero_miembros_pendientes(self):
        return self.get_query_set().values('nombre').annotate(miembros_pendientes=Count('pk')).filter(miembro__activo=False)

class Repositorio(models.Model):
    #creador     = models.ForeignKey(User, related_name="repositorios_creados", verbose_name=_("creador"))
    nombre       = models.CharField(max_length=100, unique=True)
    descripcion  = models.CharField(max_length=100)
    fecha        = models.DateTimeField(default=datetime.now, blank=True)
    direccionWeb = models.URLField(verify_exists=False)
    emailAdmin   = models.EmailField()
    miembros     = models.ManyToManyField(User, through="Miembro")
    activo       = models.BooleanField(_("activo"), default=True)
    objects      = DefaultRepositorioManager()
    miem         = RepositorioManager()
    
    def get_absolute_url(self):
        return '%sdetalle/%s/'%(app_settings.REPOSITORY_URL_BASE, self.nombre)
        
    def __unicode__(self):
        return "%s"%(self.nombre)
        
class Miembro(models.Model):
    
    fecha_ingreso   = models.DateTimeField(default=datetime.now)
    usuario         = models.ForeignKey(User)
    repositorio     = models.ForeignKey(Repositorio)
    creador         = models.BooleanField(_("Es creador?"), default=False)
    activo          = models.BooleanField(_("activo"), default=False) #El creador del repositorio decidira a quien bloquear
    
    #class Meta:
        #ordering = ('-fecha_ingreso')
        
    def get_absolute_url(self):
        return "%ssdfgdf"

    def __unicode__(self):
        return "%s miembro de %s"%(self.usuario.username, self.repositorio.nombre)


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

class Mensaje(models.Model):
    usuario     = models.ForeignKey(User)
    repositorio = models.ForeignKey(Repositorio)
    fecha       = models.DateTimeField(default=datetime.now)
    tipo        = models.CharField(max_length=1, default=MENSAJE_SIMPLE, choices = MENSAJE_CHOICES)
    descripcion = models.CharField(max_length=140)

    def __unicode__(self):
        return "%s en %s"%(self.usuario.username, self.repositorio.nombre)