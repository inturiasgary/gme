from django.conf import settings
from django import forms

from perfiles.models import Perfil

try:
    from notification import models as notification
except ImportError:
    notification = None

class PerfilForm(forms.ModelForm):
    
    class Meta:
        model = Perfil
        exclude = ('user',) #excluimos user para que no se muestre en el formulario
