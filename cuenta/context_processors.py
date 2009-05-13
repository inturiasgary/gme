from cuenta.models import Cuenta, AnonymousAccount

def cuenta(request):
    if request.user.is_authenticated():
        try:
            cuenta = Cuenta._default_manager.get(user=request.user)
        except Cuenta.DoesNotExist:
            cuenta = AnonymousAccount(request)
    else:
        cuenta = AnonymousAccount(request)
    return {'cuenta': cuenta}
