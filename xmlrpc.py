#!/usr/bin/env python
#-*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from repositorio.models import Repositorio, Mensaje, Miembro, MENSAJE_COMMIT 
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
        response.write("Metodos disponibles mediante XML-RPC!<br>")
        response.write("Los siguientes metodos estan disponibles:<ul>")
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
    '''Verifica la autentucidad del usuario en el sistema'''
    try:
        usuario = User.objects.get(username=usuario)
        if usuario.check_password(password):
            return True
        else:
            return False
    except:
        return False

def verificar_pertenece(usuario, repositorio):
    '''Verifica si es miembro o no del determinado repositorio'''
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

def publicarEntrada(usuario, password, contenido):
    '''Permite publicar un anuncio en el microblog global, parametros que recibe: (usuario, password, contenido)'''
    try:
        if verificar_password(usuario, password):
            usuario = User.objects.get(username=usuario)
            e = Entrada.objects.create(user=usuario, contenido=contenido)
            return ("Operacion efectuada, Se publicó correctamente.")
        else:
            return "Nombre de usuario o password incorrecto."
    except:
        return "Nombre de usuario no registrado."

def estadosRepo(usuario, password, repositorio):
    ''' visualiza los anuncios publicados en un determinado repositorio, parametros que recibe:(usuario, password, repositorio)'''
    if verificar_password(usuario, password):
        if verificar_pertenece(usuario, repositorio):
            '''extraemos la lista de publicaciones en el repositorio '''
            lista_commits = list(Mensaje.objects.order_by('-fecha').filter(repositorio__nombre=repositorio).values('usuario__username','descripcion'))
            if len(lista_commits)==0:
                return "No hay anuncios en el repositorio"
            return lista_commits
        else:
            return 'Error: Usuario no es miembro del repositorio, o repositorio no existente.'
    else:
        return 'Error: Nombre de usuario o password incorrecta.'

def todoRepo(usuario, password, repositorio):
    """ Permite visualizar la lista de tareas incompletas de un determinado repositorio, parametros que recibe: (usuario, password, repositorio)"""
    try:
        if verificar_password(usuario, password):
            if verificar_pertenece(usuario, repositorio):
                lista_tareas = list(Item.objects.filter(assigned_to__username=usuario, completed=False, list__grupo__nombre=repositorio).values('title','assigned_to__username'))
                return lista_tareas 
            else:
                return "Error: Usuario no pertenece al repositorio o no esta activo."
        else:
            return "Error: El usuario no esta registrado en el sistema"
    except:
        return "Error: Problemas"

def publicarCommit(nombre_repo, usuario, password, descripcion):
    if verificar_password(usuario, password):
        if verificar_pertenece(usuario, nombre_repo):
            usuario = User.objects.get(username=usuario)
            repositorio = Repositorio.objects.get(nombre=nombre_repo)
            try:
                Mensaje.objects.create(usuario=usuario, repositorio= repositorio, descripcion=descripcion, tipo='c')
                return "Operacion efectuada correctamente, se publico al sistema web."
            except:
                return "Error: Commit no creado en sistema."
        else:
            return "Nombre de usuario no pertenece al repositorio."
    else:
        return "Nombre de usuario o password incorrecto."

#registracion de metodos que pueden ser llamados mediante el protocolo XML-RPC
#dispatcher.register_function(crearRepositorio,'crearRepositorio')
dispatcher.register_function(publicarEntrada,'publicarEntrada')
dispatcher.register_function(publicarCommit,'publicarCommit')
dispatcher.register_function(estadosRepo, 'estadosRepo')
dispatcher.register_function(todoRepo, 'todoRepo')