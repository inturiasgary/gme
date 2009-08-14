from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class Perfil(models.Model):

    user       = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    nombre     = models.CharField(_('nombre'), max_length=50, null=True, blank=True)
    comentario = models.TextField(_('comentario'), null=True, blank=True)
    ubicacion  = models.CharField(_('ubicacion'), max_length=40, null=True, blank=True)
    sitioWeb   = models.URLField(_('sitio web'), null=True, blank=True, verify_exists=False)
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return ('detalle_perfil', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name        = _('perfil')
        verbose_name_plural = _('perfiles')

def create_perfil(sender, instance=None, **kwargs):
    ''' Para cada usuario creado, se crea un perfil '''
    if instance is None:
        return
    perfil, created = Perfil.objects.get_or_create(user=instance)

post_save.connect(create_perfil, sender=User)
