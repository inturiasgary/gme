#!/usr/bin/env python
#-*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from repositorio.models import Repositorio, Mensaje, Miembro
from microblog.models import Entrada
from todo.models import Item
import sys

#Verificamos la version de python instalada para la creacion del dispatcher
if sys.version_info[:3] >= (2,5,):
    dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5 o mayor
else:
    dispatcher = SimpleXMLRPCDispatcher()

def rpc_handler(request):
    """
    Escuchador actual:
    mediante el urls.py, todas las llamadas del servicio xml-rpc pueden ser
    enrutadas por aqui.
    """
    response = HttpResponse()
    if request.POST:
        try:
            response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
        except Exception, e:
            return HttpResponseServerError()
    else:
        #TODO Realizar descripcion del servicio
        response.write("<b>Servicio XML-RPC ofrecido por el sistema web GME.</b><br>")
        response.write("Metodos disponibles mediante XML-RPC!<br><ul>")
        methods = dispatcher.system_listMethods()
        for method in methods:
            sig = dispatcher.system_methodSignature(method)
            help =  dispatcher.system_methodHelp(method)
            #response.write("<li><b>%s</b>: [%s] %s" % (method, help))
            response.write("<li><b>%s</b>: %s</li>" % (method,help))
        response.write("</ul>")
    response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')
    response['Content-length'] = str(len(response.content))
    return response

def verificar_password(usuario, password):
    '''Verifica la autenticidad del usuario en el sistema'''
    try:
        usuario = User.objects.get(username=usuario)
        if usuario.check_password(password):
            return True
        else:
            return False
    except:
        return False

def verificar_pertenece(usuario, repositorio):
    '''verificar_pertenece(usuario, repositorio)<p>Permite verificar si un usuario es miembro activo de un repositorio dado.</p><p>Parámetros:</p><p><ul><li>usuario: nombre de usuario con el que esta registrado en el sistema.</li><li>repositorio: nombre del repositorio con el cual esta registrado en el sistema.</li></ul></p>'''
    try:
        miembro = Miembro.objects.filter(repositorio__nombre=repositorio, usuario__username = usuario, activo=True)
        if miembro:
            return True
        else:
            return False
    except:
        return False

#TODO esta funcion aun incompleta
def crearRepositorio(usuario, nombre,descripcion,direccionWeb,emailAdmin):
    '''Permite la creacion de forma remota de repositorios'''
    usuario = User.objects.get(username=usuario)
    repositorio = Repositorio.objects.create(nombre=nombre,descripcion=descripcion,direccionWeb=direccionWeb,emailAdmin=emailAdmin)
    miembro = Miembro.objects.create(usuario=usuario,repositorio=repositorio, creador=True, activo=True)
    return True

def publicarAnuncio(usuario, password, contenido):
    '''publicarAnuncio(usuario, password, contenido)<p>Permite publicar un anuncio en el microblog global.</p><p>Parámetros:</p><p><ul><li>usuario: nombre de usuario con el que esta registrado en el sistema.</li><li>password: contraseña con el cual esta registrado en el sistema.</li><li>contenido: El contenido texto de un comentario.</li></ul></p>'''
    try:
        if verificar_password(usuario, password):
            usuario = User.objects.get(username=usuario)
            Entrada.objects.create(user=usuario, contenido=contenido)
            return ("Nota: Operación efectuada, Se publicó correctamente.")
        else:
            return "Error: Nombre de usuario o contraseña incorrecta."
    except:
        return "Error: Nombre de usuario no registrado."

def anunciosMicro(usuario, password):
    '''anunciosMicro(usuario, password)<p>Retorna una lista de los ultimos diez anuncios publicados en el microblog global.</p><p>Parámetros:</p><p><ul><li>usuario: nombre de usuario con el que esta registrado en el sistema.</li><li>password: contraseña con el cual esta registrado en el sistema.</li></ul></p>'''
    if verificar_password(usuario, password):
        lista_entrada = list(Entrada.objects.order_by('-fecha').filter(recipientes__username=usuario).values('user__username', 'contenido')[:10])
        if len(lista_entrada)==0:
            return "Nota: No hay lista de publicaciones en el microblog global."
        else:
            return lista_entrada
    else:
        return 'Error: Nombre de usuario o contraseña incorrecta.' 

def anunciosRepo(usuario, password, repositorio):
    '''anunciosRepo(usuario, password, repositorio)<p>Retorna una lista de los ultimos diez anuncios publicados en el repositorio dado.</p><p>Parámetros:</p><p><ul><li>usuario: nombre de usuario con el que esta registrado en el sistema.</li><li>password: contraseña con el cual esta registrado en el sistema.</li><li>repositorio: nombre del repositorio con el cual esta registrado en el sistema</li></ul></p>'''
    if verificar_password(usuario, password):
        if verificar_pertenece(usuario, repositorio):
            '''extraemos la lista de publicaciones en el repositorio '''
            lista_commits = list(Mensaje.objects.order_by('-fecha').filter(repositorio__nombre=repositorio).values('usuario__username','descripcion')[:10])
            if len(lista_commits)==0:
                return "Nota: No hay anuncios en el repositorio."
            return lista_commits
        else:
            return 'Error: Usuario no es miembro del repositorio, o repositorio no existe.'
    else:
        return 'Error: Nombre de usuario o contraseña incorrecta.'

def todoRepo(usuario, password, repositorio):
    '''todoRepo(usuario, password, repositorio)<p>Retorna la lista de tareas incompletas asignadas a un usuario en el repositorio dado.</p><p>Parámetros:</p><p><ul><li>usuario: nombre de usuario con el que esta registrado en el sistema.</li><li>password: contraseña con el cual esta registrado en el sistema.</li><li>repositorio: nombre del repositorio con el cual esta registrado en el sistema.</li></ul></p>'''
    try:
        if verificar_password(usuario, password):
            if verificar_pertenece(usuario, repositorio):
                lista_tareas = list(Item.objects.filter(assigned_to__username=usuario, completed=False, list__grupo__nombre=repositorio).values('title'))
                return lista_tareas 
            else:
                return "Error: Usuario no pertenece al repositorio o no esta activo."
        else:
            return "Error: El usuario no esta registrado en el sistema"
    except:
        return "Error: Problemas"

def publicarCommit(nombre_repo, usuario, password, descripcion, tipo):
    '''publicarCommit(nombre_repo, usuario, password, descripcion, tipo)<p>Permite publicar un anuncio en el microblog de repositorios, tipo determina la categoría de anuncio a mostrar.</p><p>Parámetros:</p><p><ul><li>nombre_repo: nombre del repositorio con el cual esta registrado en el sistema.</li><li>usuario: nombre de usuario con el que esta registrado en el sistema.</li><li>password: contraseña con el cual esta registrado en el sistema.</li><li>descripcion: El contenido texto de un comentario, detalla la descripción de la publicación.</li><li>tipo: especifica que tipo de anuncio se  publicará, opciones: r internas del repositorio, s anuncios efectuados en el sistema, c anuncio común.</li></ul></p>'''

    if verificar_password(usuario, password):
        if verificar_pertenece(usuario, nombre_repo):
            usuario = User.objects.get(username=usuario)
            repositorio = Repositorio.objects.get(nombre=nombre_repo)
            try:
                Mensaje.objects.create(usuario=usuario, repositorio= repositorio, descripcion=descripcion, tipo=tipo)
                return "Operación efectuada correctamente, se publicó al sistema web."
            except:
                return "Error: Commit no creado en sistema."
        else:
            return "Nombre de usuario no pertenece al repositorio."
    else:
        return "Nombre de usuario o contraseña incorrecta."

#registracion de metodos que pueden ser llamados mediante el protocolo XML-RPC
#dispatcher.register_function(crearRepositorio,'crearRepositorio')
dispatcher.register_function(publicarAnuncio,'publicarAnuncio')
dispatcher.register_function(publicarCommit,'publicarCommit')
dispatcher.register_function(anunciosRepo, 'anunciosRepo')
dispatcher.register_function(todoRepo, 'todoRepo')
dispatcher.register_function(verificar_pertenece, 'verificar_pertenece')
dispatcher.register_function(anunciosMicro, 'anunciosMicro')
