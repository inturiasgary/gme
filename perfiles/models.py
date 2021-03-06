from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from utils.stdimage import fields
import datetime
from utils import uploads

class Perfil(models.Model):

    user         = models.OneToOneField(User, unique=True, verbose_name=_('user'))
    nombre       = models.CharField(_('Name'), max_length=50, null=True, blank=True)
    comentario   = models.TextField(_('Comment'), null=True, blank=True)
    ubicacion    = models.CharField(_('Address'), max_length=40, null=True, blank=True)
    sitioWeb     = models.URLField(_('Web Site'), null=True, blank=True, verify_exists=False)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True )
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return ('detalle_perfil', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name        = _('profile')
        verbose_name_plural = _('profiles')

def create_perfil(sender, instance=None, **kwargs):
    ''' Para cada usuario creado, se crea un perfil '''
    if instance is None:
        return
    perfil, created = Perfil.objects.get_or_create(user=instance)

post_save.connect(create_perfil, sender=User)
