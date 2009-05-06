from django.core.management.base import NoArgsCommand
from perfiles.models import Perfil
from django.contrib.auth.models import User
from django.conf import settings

class Command(NoArgsCommand):
    help = 'Create a profile object for users which do not have one.'

    def handle_noargs(self, **options):
        for usr in User.objects.all():
            profile, is_new = Perfil.objects.get_or_create(user=usr)
            if is_new: perfil.save()
