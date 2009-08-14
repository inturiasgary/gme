import random, string
from django.contrib.contenttypes.models import ContentType
from datetime import date

def get_path(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    model = ctype.model
    extension = filename.split('.')[-1]
    dir = "uploads"
    if model == "perfil" or model =="Perfil":
        dir += "/images/users/%s" % instance.user.username
    else:
        dir += "/documents/%s" % model
        if model == "applicant":
            filename = u"%s.%s" % (instance.ssn, extension)
    return "%s/%s" % (dir, filename)