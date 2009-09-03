from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.contrib.auth.models import User
from repositorio.models import *
from microblog.models import *
from todo.models import *
import sys
from django.utils.translation import ugettext_lazy as _
#from django.core import serializers #no usado
from xml.dom.minidom import Document #para crear el contenido en xml

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
	
def verificar_pertenece(usuario, repositorio):
	miembro = Miembro.objects.filter(repositorio__nombre=repositorio, usuario__username = usuario, activo=True)
	if miembro:
		return True
	else:
		return False
	
def verificar_password(usuario, password):
	usuario = User.objects.get(username=usuario)
	if usuario:
		if usuario.check_password(password):
			return True
		else:
			return False
	return False
	
def estadosRepo(usuario, password, repositorio):
	''' visualioza los anuncios publicados en un determinado repositorio '''
	if verificar_password(usuario, password):
		if verificar_pertenece(usuario, repositorio):
			''' extraemos la lista de publicaciones en el repositorio '''
			lista_commits = Commit.objects.filter(repositorio__nombre=repositorio)
			#lista_commits = serializers.serialize("xml", Commit.objects.filter(repositorio__nombre=repositorio), 
			#				      fields=('usuario','fecha', 'descripcion'))
			doc = Document()
			commit = doc.createElement('Commits')
			doc.appendChild(commit)
			main = doc.createElement('autores')
			commit.appendChild(main)
			for lista_commit in lista_commits:
				creador = doc.createElement('autor')
				main.appendChild(creador)
				ptext = doc.createTextNode(lista_commit.usuario.username)
				creador.appendChild(ptext)
				mensaje = doc.createElement('mensaje')
				men = doc.createTextNode(lista_commit.descripcion)
				mensaje.appendChild(men)
				main.appendChild(mensaje)
				
				print lista_commit.usuario.username
				

			print doc.toprettyxml(indent="  ")
			
			
			return doc.toprettyxml(indent="  ")
		else:
			return 'Repositorio no existente o usuario no pertenece.'
	else:
		print 'nombre de usuario o contrasenia incorrecta'

	
def todoRepo(usuario, password, repositorio):
	try:
		''' permite visualizar los estados en el repositorio correspondiente '''
		usuario = User.objects.get(username=usuario)
		print "1 crea usuario"
		#repositorio = repositorio.objects.get(nombre=repositorio)
		
		if usuario.check_password(password):
			si = True
			miembro = Miembro.objects.filter(repositorio__nombre=repositorio, usuario=usuario, activo=True)
			print "2 revisa miembro"
			if miembro:
				print "es miembro."
				lista_tareas = Item.objects.filter(assigned_to=usuario, completed=0, list__grupo__nombre = repositorio )
				lista = {}
				for i in lista_tareas:
					lista['tarea'] = i.title
					
				return lista
			else:
				return "no pertenece al repositorio o no esta activo."
		else:
			si = False
		if si:
			e = Entrada(user=usuario, contenido=contenido)
			e.save()
			return "Operacion efectuada correctamente."
		else:
			return "Nombre de usuario o password incorrrecto."
	except:
		''' '''
		return "El repositorio no existe"

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
dispatcher.register_function(estadosRepo, 'estadosRepo')