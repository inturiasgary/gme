from django.utils.cache import patch_vary_headers
from django.utils import translation
from cuenta.models import Cuenta

class LocaleMiddleware(object):
    """
    Este es un simple middleware que pasa un request y decide
    que objeto traducido va a determinar en el actual hilo context
    dependiendo de la cuenta de usuario. esto permite
    a las paginas traducirse de forma automatica al lenguaje 
    seleccionado por el usuario
    """
    def get_language_for_user(self, request):
        if request.user.is_authenticated():
            try:
                cuenta = Cuenta.objects.get(user=request.user)
                return cuenta.language
            except Cuenta.DoesNotExist:
                pass
        return translation.get_language_from_request(request)

    def process_request(self, request):
        translation.activate(self.get_language_for_user(request))
        request.LANGUAGE_CODE = translation.get_language()  #establece el lenguaje

    def process_response(self, request, response): #establece el lenguaje a ser traducido
        patch_vary_headers(response, ('Accept-Language',))
        response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
