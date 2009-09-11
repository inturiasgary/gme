from datetime import datetime
from django.db import models
import app_settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Constantes para establecer los estados de las conexiones
CONEXION_ESPERANDO = 'e'
CONEXION_ACEPTADA = 'a'
CONEXION_BLOQUEADA = 'b'

CONEXION_ESTADOS = (
    (CONEXION_ESPERANDO, _('Esperando')),
    (CONEXION_ACEPTADA, _('Aceptada')),
    (CONEXION_BLOQUEADA, _('Bloqueada')),
)

#import app_settings, msn

class Entrada(models.Model):
    ''' Permite almacenar los anuncios de los usuarios, podran ser vistas por sus conecciones aceptadas
    
    # Creacion de algunas entradas
    >>> from django.contrib.auth.models import User
    >>> usuario = User.objects.create(username="gary")
    >>> entradaPrueba = Entrada.objects.create(user=usuario, contenido="Entrada de prueba")
    >>> print entradaPrueba.contenido
    Entrada de prueba
    '''
    class Meta:
        ordering = ('-fecha',)

    user        = models.ForeignKey(User)
    contenido   = models.TextField(max_length=140)
    recipientes = models.ManyToManyField(User, related_name='entradas_recibidos')
    fecha       = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return '%se/%d/'%(app_settings.MICROBLOG_URL_BASE, self.id)

    def __unicode__(self):
        return "%s @ %s"%(self.user.username, self.fecha)
    

class Conexion(models.Model):
    ''' Permite guardar las relaciones establecidas entre los usuarios, pueden ser en espera, aceptados o bloqueados'''
    user = models.ForeignKey(User, related_name='conexiones_desde')
    amigo = models.ForeignKey(User, related_name='conexiones_hacia')
    estado = models.CharField(
            max_length=1,
            default=CONEXION_ESPERANDO,
            blank=True,
            choices=CONEXION_ESTADOS,
            )
    fecha = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return "%s -> %s"%(self.user.username, self.amigo.username)

    def get_absolute_url(self):
        return '%sc/%d/'%(app_settings.MICROBLOG_URL_BASE, self.id)

class MicroblogUserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    msn_id = models.CharField(max_length=50, blank=True)
    gtalk_id = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.user.username

# SENALES
from django.db.models import signals

# ENTRADAS

def entrada_post_save(sender, instance, signal, *args, **kwargs):
    if not kwargs.get('created'):
        return

    # Se adiciona el usuario a si mismo a la lista de recipientes
    instance.recipientes.add(instance.user)

    # Adiciona a sus amigos a la lista de recipientes
    for conexion in instance.user.conexiones_hacia.filter(estado=CONEXION_ACEPTADA):
        instance.recipientes.add(conexion.user)

    # envion al menssenger, aun no funciona
    #if app_settings.MICROBLOG_MESSENGERS_ENABLED:
        #instance.send_to_messengers()

signals.post_save.connect(entrada_post_save, sender=Entrada)

# Conexiones

def conexion_post_save(sender, instance, signal, *args, **kwargs):
    if not kwargs.get('created'):
        return

    Conexion.objects.get_or_create(amigo=instance.user, user=instance.amigo)

signals.post_save.connect(conexion_post_save, sender=Conexion)

# MicroblogUserProfile

#def user_post_save(sender, instance, signal, *args, **kwargs):
    #up = MicroblogUserProfile.objects.get_or_create(usuario=instance)

#signals.post_save.connect(usuario_post_save, sender=User)

