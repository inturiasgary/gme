from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from repositorio.models import Repositorio, Mensaje, Miembro, MENSAJE_COMMIT 
from microblog.models import Entrada
from django.utils.translation import ugettext_lazy as _
from xml.dom.minidom import Document #para crear el contenido en xml
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
    try:
        usuario = User.objects.get(username=usuario)
        if usuario.check_password(password):
            return True
        else:
            return False
    except:
        return False

def verificar_pertenece(usuario, repositorio):
    try:
        miembro = Miembro.objects.filter(repositorio__nombre=repositorio, usuario__username = usuario, activo=True)
        if miembro:
            return True
        else:
            return False
    except:
        return False

def crearRepositorio(usuario, nombre,descripcion,direccionWeb,emailAdmin):
    '''Permite la creacion de forma remota de repositorios'''
    #TODO Completar la esta funcion
    usuario = User.objects.get(username=usuario)
    repositorio = Repositorio.objects.create(nombre=nombre,descripcion=descripcion,direccionWeb=direccionWeb,emailAdmin=emailAdmin)
    miembro = Miembro.objects.create(usuario=usuario,repositorio=repositorio, creador=True, activo=True)
    return True

def publicarEntrada(usuario, password, contenido):
    '''Permite publicar un anuncio en el microblog global, parametros que recibe: (usuario, password, contenido)'''
    try:
        usuario = User.objects.get(username=usuario)
        if usuario.check_password(password):
            e = Entrada.objects.create(user=usuario, contenido=contenido)
            return _("Operacion efectuada correctamente.")
        else:
            return _("Nombre de usuario o password incorrecto.")
    except:
        return _("Nombre de usuario no registrado.")

def estadosRepo(usuario, password, repositorio):
    ''' visualiza los anuncios publicados en un determinado repositorio, parametros que recibe:(usuario, password, repositorio)'''
    if verificar_password(usuario, password):
        if verificar_pertenece(usuario, repositorio):
            '''extraemos la lista de publicaciones en el repositorio '''
            lista_commits = Mensaje.objects.order_by('-fecha').filter(repositorio__nombre=repositorio)
            #lista_commits = serializers.serialize("xml", Commit.objects.filter(repositorio__nombre=repositorio), 
            #fields=('usuario','fecha', 'descripcion'))
            oc = Document()
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
            return doc.toprettyxml(indent="  ")
        else:
            return _('Repositorio no existente o usuario no pertenece.')
    else:
        return _('nombre de usuario opassword incorrecta.')
        
def todoRepo(usuario, password, repositorio):
    """ Permite visualizar las tareas incompletas de un determinado repositorio,parametros que recibe: (usuario, password, repositorio)"""
    try:
        ''' permite visualizar los estados en el repositorio correspondiente '''
        if verificar_password(usuario, password):
            if verificar_pertenece(usuario, repositorio):
                lista_tareas = Item.objects.filter(assigned_to__username=usuario, completed=False, list__grupo__nombre=repositorio)
                doc = Document()
                todo = doc.createElement('ToDo')
                doc.appendChild(todo)
                tar = doc.createElement('tarea')
                todo.appendChild(tar)
                for tarea in lista_tareas:
                    titulo = doc.createElement('titulo')
                    tar.appendChild(titulo)
                    ptext = doc.createTextNode(tarea.title)
                    titulo.appendChild(ptext)
                    hacerHasta = doc.createElement('HacerHasta')
                    men = doc.createTextNode('%s/%s/%s'%(tarea.due_date.day , tarea.due_date.month, tarea.due_date.year))
                    hacerHasta.appendChild(men)
                    tar.appendChild(hacerHasta)
                return doc.toprettyxml(indent="  ")
            else:
                return _("no pertenece al repositorio o no esta activo.")
        else:
            return _("El usuario no esta registrado en el sistema")
    except:
        return _("Problemas")

def publicarCommit(nombre_repo, usuario, password, descripcion):
        if verificar_password(usuario, password):
            if verificar_pertenece(usuario, nombre_repo):
                try:
                    Mensaje.objects.create(usuario=usuario, repositorio= repo, descripcion=descripcion, tipo=MENSAJE_COMMIT)
                    return _("Operacion efectuada correctamente.")
                except:
                    return _("Error en la creacion del commit")
            else:
                return _("Nombre de usuario no pertenece al repositorio.")
        else:
            return _("Nombre de usuario o password incorrecto.")

#registracion de metodos que pueden ser llamados mediante el protocolo XML-RPC
dispatcher.register_function(crearRepositorio,'crearRepositorio')
dispatcher.register_function(publicarEntrada,'publicarEntrada')
dispatcher.register_function(publicarCommit,'publicarCommit')
dispatcher.register_function(estadosRepo, 'estadosRepo')
dispatcher.register_function(todoRepo, 'todoRepo')
