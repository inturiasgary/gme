from cuenta.models import Cuenta, CuentaAnonima

def cuenta(request):
    if request.user.is_authenticated():
        try:
            cuenta = Cuenta._default_manager.get(user=request.user)
        except Cuenta.DoesNotExist:
            cuenta = CuentaAnonima(request)
    else:
        cuenta = CuentaAnonima(request)
    return {'cuenta': cuenta}
