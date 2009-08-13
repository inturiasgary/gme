from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.contrib.auth.models import User
from repositorio.models import *
from microblog.models import *
import sys
from django.utils.translation import ugettext_lazy as _
#Verificamos la version de python instalada para la creacion del dispatcher
if sys.version_info[:3] >= (2,5,):
	dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5 o mayor
else:
	dispatcher = SimpleXMLRPCDispatcher()

def rpc_handler(request):
	"""
	the actual handler:
	if you setup your urls.py properly, all calls to the xml-rpc service
	should be routed through here.
	If post data is defined, it assumes it's XML-RPC and tries to process as such
	Empty post assumes you're viewing from a browser and tells you about the service.
	"""

	response = HttpResponse()
	if len(request.POST):
		response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
	else:
		response.write("<b>Servicio XML-RPC ofrecido por el sistema web GME.</b><br>")
		response.write("Metodos disponibles mediante XML-RPC!<br>")
		response.write("Los siguientes metodos estan disponibles:<ul>")
		methods = dispatcher.system_listMethods()

		for method in methods:
			sig = dispatcher.system_methodSignature(method)
			help =  dispatcher.system_methodHelp(method)

			response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

		response.write("</ul>")
		response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')

	response['Content-length'] = str(len(response.content))
	return response

def crearRepositorio(usuario, nombre,descripcion,direccionWeb,emailAdmin):
	usuario = User.objects.get(username=usuario)
	repositorio = Repositorio(nombre=nombre,descripcion=descripcion,direccionWeb=direccionWeb,emailAdmin=emailAdmin)
	repositorio.save()
	miembro = Miembro(usuario=usuario,repositorio=repositorio, creador=True, activo=True)
	miembro.save()
	return True

def publicarEntrada(usuario, password, contenido):
	try:
		usuario = User.objects.get(username=usuario)
		if usuario.check_password(password):
			si = True
		else:
			si = False
		if si:
			e = Entrada(user=usuario, contenido=contenido)
			e.save()
			return "Operacion efectuada correctamente."
		else:
			return "Nombre de usuario o password incorrecto."
	except:
		return "Nombre de usuario no registrado."

def publicarCommit(nombre_repo, usuario, password, descripcion):
	try:
		usuario = User.objects.get(username=usuario)
		repo = Repositorio.objects.get(nombre=nombre_repo)
		if usuario.check_password(password):
			si = True
		else:
			si = False
		if si:
			try:
				miembro = Miembro.objects.get(usuario=usuario, repositorio=repo, activo = True)
				if miembro:
					e = Commit(usuario=usuario, repositorio=repo, descripcion=descripcion)
					e.save()
			except:
				return "Error en la creacion del commit"
			return "Operacion efectuada correctamente."
		else:
			return "Nombre de usuario o password incorrecto."
	except:
		return "Nombre de usuario no registrado."
#registracion de metodos que pueden ser llamados mediante el protocolo XML-RPC	
dispatcher.register_function(crearRepositorio,'crearRepositorio')
dispatcher.register_function(publicarEntrada,'publicarEntrada')
dispatcher.register_function(publicarCommit,'publicarCommit')