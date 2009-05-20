from django.utils.cache import patch_vary_headers
from django.utils import translation
from cuenta.models import Cuenta

class LocaleMiddleware(object):
    """
    Este es un simple middleware que pasa un request y decide
    que objeton traducido va a instalar en el actual hilo context
    dependiendo de la cuenta de usuario. esto permite
    a las paginas traducirse de forma dinamica al lenguaje 
    seleccionado por el usuario
    """
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context depending on the user's account. This allows pages
    to be dynamically translated to the language the user desires
    (if the language is available, of course). 
    """

    def get_language_for_user(self, request):
        if request.user.is_authenticated():
            try:
                cuenta = Cuenta.objects.get(user=request.user)
                return cuenta.lenguaje
            except Cuenta.DoesNotExist:
                pass
        return translation.get_language_from_request(request)

    def process_request(self, request):
        translation.activate(self.get_language_for_user(request))
        request.LANGUAGE_CODE = translation.get_language()  #establece el lenguaje

    def process_response(self, request, response): #estable el lenguaje a ser traducido
        patch_vary_headers(response, ('Accept-Language',))
        response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
