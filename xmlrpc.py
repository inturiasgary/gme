# Patchless XMLRPC Service for Django
# Kind of hacky, and stolen from Crast on irc.freenode.net:#django
# Self documents as well, so if you call it from outside of an XML-RPC Client
# it tells you about itself and its methods
#
# Brendan W. McAdams <brendan.mcadams@thewintergrp.com>

# SimpleXMLRPCDispatcher lets us register xml-rpc calls w/o
# running a full XMLRPC Server.  It's up to us to dispatch data

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.contrib.auth.models import User
from repositorio.models import *
# Create a Dispatcher; this handles the calls and translates info to function maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5

 

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
			# right now, my version of SimpleXMLRPCDispatcher always
			# returns "signatures not supported"... :(
			# but, in an ideal world it will tell users what args are expected
			sig = dispatcher.system_methodSignature(method)

			# this just reads your docblock, so fill it in!
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
	

def oracion(a):
	print "Palabra recibida %s"%a
	return a


# you have to manually register all functions that are xml-rpc-able with the dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it from the XML-RPC side...
dispatcher.register_function(oracion, 'oracion')
dispatcher.register_function(crearRepositorio,'crearRepositorio')