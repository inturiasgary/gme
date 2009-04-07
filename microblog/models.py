from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

import app_settings, msn

class Anuncio(models.Model):
    ''' Permite almacenar los anuncios de los usuarios, podran ser vistas por sus conecciones aceptadas'''
    class Meta:
        ordering = ('-fecha',)

    usuario = models.ForeignKey(User)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return '%se/%d/'%(app_settings.MICROBLOG_URL_BASE, self.id)

    def __unicode__(self):
        return "%s @ %s"%(self.user.username, self.date)
    

# Constantes para establecer los estados de las conexiones
CONEXION_ESPERANDO = 'e'
CONEXION_ACEPTADA = 'a'
CONEXION_BLOQUEADA = 'b'

CONEXION_ESTADOS = (
    (CONEXION_ESPERANDO, _('Esperando')),
    (CONEXION_ACEPTADA, _('Aceptada')),
    (CONEXION_BLOQUEADA, _('Bloqueada')),
)

class Conexion(models.Model):
    ''' Permite guardar las relaciones establecidas entre los usuarios, pueden ser en espera, aceptados o bloqueados'''
    usuario = models.ForeignKey(User, related_name='conexiones_desde')
    amigo = models.ForeignKey(User, related_name='conexiones_hacia')
    estado = models.CharField(
            max_length=1,
            default=CONEXION_ESPERANDO,
            blank=True,
            choices=CONEXION_ESTADOS,
            )
    fecha = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return "%s -> %s"%(self.usuario.username, self.amigo.username)

    def get_absolute_url(self):
        return '%sc/%d/'%(app_settings.MICROBLOG_URL_BASE, self.id)

class MicroblogUserProfile(models.Model):
    usuario = models.ForeignKey(User, unique=True)
    msn_id = models.CharField(max_length=50, blank=True)
    gtalk_id = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.user.username

# SEÑALES
from django.db.models import signals

# ENTRADAS

def entry_post_save(sender, instance, signal, *args, **kwargs):
    if not kwargs.get('created'):
        return

    # Add user itself to recipients list
    instance.recipients.add(instance.user)

    # Add user friends to recipients list
    for connection in instance.user.connections_to.filter(status=CONNECTION_ACCEPTED):
        instance.recipients.add(connection.user)

    # Send to messengers
    if app_settings.MICROBLOG_MESSENGERS_ENABLED:
        instance.send_to_messengers()

signals.post_save.connect(entry_post_save, sender=Entry)

# Connection

def connection_post_save(sender, instance, signal, *args, **kwargs):
    if not kwargs.get('created'):
        return

    Connection.objects.get_or_create(friend=instance.user, user=instance.friend)

signals.post_save.connect(connection_post_save, sender=Connection)

# MicroblogUserProfile

def user_post_save(sender, instance, signal, *args, **kwargs):
    up = MicroblogUserProfile.objects.get_or_create(user=instance)

signals.post_save.connect(user_post_save, sender=User)

