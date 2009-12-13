from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save #para enviar senales depues del guardado de informacion
from django.utils.translation import get_language_from_request, ugettext_lazy as _ #para la internacionalizacion

from timezones.fields import TimeZoneField  #para utilizar campos de zona horaria

class Cuenta(models.Model):
    
    user        = models.ForeignKey(User, unique=True, verbose_name=_('Username'))
    timezone    = TimeZoneField(_('Timezone'))
    language    = models.CharField(_('Language'), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    
    def __unicode__(self):
        return self.user.username

def create_Cuenta(sender, instance=None, **kwargs): #asocia al usuario creado, con la cuenta
    ''' Realiza la creacion de una cuenta para cada usuario nuevo registrado '''
    if instance is None:
        return
    cuenta, created = Cuenta.objects.get_or_create(user=instance)

post_save.connect(create_Cuenta, sender=User)

class CuentaAnonima(object):
    def __init__(self, request=None):
        self.user = AnonymousUser()
        self.timezone = settings.TIME_ZONE
        if request is not None:
            self.language = get_language_from_request(request)
        else:
            self.language = settings.LANGUAGE_CODE

    def __unicode__(self):
        return "CuentaAnonima"
