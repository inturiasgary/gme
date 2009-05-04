from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save #para enviar senales depues del guardado de informacion
from django.utils.translation import get_language_from_request, ugettext_lazy as _ #para la internacionalizacion

from timezones.fields import TimeZoneField  #para utilizar campos de zona horaria

class Cuenta(models.Model):
    
    usuario = models.ForeignKey(User, unique=True, verbose_name=_('usuario'))
    timezone = TimeZoneField(_('timezone'))
    lenguaje = models.CharField(_('lenguaje'), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    
    def __unicode__(self):
        return self.usuario.username

def create_Cuenta(sender, instance=None, **kwargs): #asocia al usuario creado con la cuenta
    if instance is None:
        return
    cuenta, created = Cuenta.objects.get_or_create(usuario=instance)

post_save.connect(create_Cuenta, sender=User)

class AnonymousAccount(object):
    def __init__(self, request=None):
        self.user = AnonymousUser()
        self.timezone = settings.TIME_ZONE
        if request is not None:
            self.language = get_language_from_request(request)
        else:
            self.language = settings.LANGUAGE_CODE

    def __unicode__(self):
        return "AnonymousAccount"


#class OtherServiceInfo(models.Model):
    
    ## eg blogrss, twitter_user, twitter_password
    
    #user = models.ForeignKey(User, verbose_name=_('user'))
    #key = models.CharField(_('Other Service Info Key'), max_length=50)
    #value = models.TextField(_('Other Service Info Value'))
    
    #class Meta:
        #unique_together = [('user', 'key')]
    
    #def __unicode__(self):
        #return u"%s for %s" % (self.key, self.user)

#def other_service(user, key, default_value=""):
    #"""
    #retrieve the other service info for given key for the given user.
    
    #return default_value ("") if no value.
    #"""
    #try:
        #value = OtherServiceInfo.objects.get(user=user, key=key).value
    #except OtherServiceInfo.DoesNotExist:
        #value = default_value
    #return value

#def update_other_services(user, **kwargs):
    #"""
    #update the other service info for the given user using the given keyword args.
    
    #e.g. update_other_services(user, twitter_user=..., twitter_password=...)
    #"""
    #for key, value in kwargs.items():
        #info, created = OtherServiceInfo.objects.get_or_create(user=user, key=key)
        #info.value = value
        #info.save()


