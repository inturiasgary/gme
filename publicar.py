#!/usr/bin/env python
'''publicar es un CLI simple para la publicacion de estados al microblog GME global.

Uso: publicar comando [opciones]

Comando:

 actualizar    Actualiza tu mensaje de estado en el sistema microblog global
 estados       Muestra todos los 10 estados ultimos publicados de tus amigos
 iniciar       Crea los correspondientes hooks para publicaciones de repositorios automaticos
 todo          Permite realizar la visualizacion de la lista todo de forma general o de un repositorio indicado
 
Opciones:

 -u, --usuario            Nombre de usuario
 -p, --password           Password
 -m, --mensaje            Mensaje
 -r, --repositorio        Repositorio
'''
import sys, os
import getopt
import xmlrpclib
from getpass import getpass
import xml.dom.minidom


try:
    from git import *
except:
    print "Error: al importar git, Instla git antes de utilizar la aplicacion"
    sys.exit(1)
    
codigo_hook = '''#!/usr/bin/env python
import sys
import urllib, urllib2
import re
import subprocess
from datetime import datetime
import xmlrpclib
import simplejson
import os

POST_URL = 'http://127.0.0.1:8000/xml_rpc_srv/'
REPO_URL = 'http://example.com'
COMMIT_URL = r'http://example.com/commit/%s'
REPO_NAME = 'gitrepo'
REPO_OWNER_NAME = 'Git U. Some'
REPO_OWNER_EMAIL = 'git@example.com'
REPO_DESC = ''

httpconf = {}
httpconf['repositorio'] = {}
httpconf['username'] = {}
httpconf['password'] = {}
httpconf['pathrepo'] = {}
    
try:
    from git import *
except:
    print "Error: al importar git, Instala git antes de utilizar la aplicacion"
    sys.exit(1)

def cargarConfiguracion():
    try:
        f=open(os.getcwd()+'/.git/hooks/config.gme')
    except IOError, e:
        print >> sys.stderr,"No se encuentra el archivo de configuracion:%s"%e
    else:
        json_lines = f.read()
        f.close()
        cfg =simplejson.loads(json_lines)
        #recuperamos la informacion del archivo de configuracio
        httpconf['repositorio']=cfg['repositorio']
        httpconf['username']=cfg['username']
        httpconf['password']=cfg['password']
        httpconf['pathrepo']=cfg['pathrepo']
        commit = recuperarCommit(pathrepo=httpconf['pathrepo'])
        enviar_commit(httpconf['repositorio'], httpconf['username'],httpconf['password'], commit)

def recuperarCommit(pathrepo):

    repo=Repo(pathrepo)
    commit = repo.commits()[0]
    mensaje_commit = commit.message
    name = commit.committer.name
    return mensaje_commit
    
def enviar_commit(repositorio, username, password, commit):
    try:
        rpc_srv = xmlrpclib.ServerProxy(POST_URL)
        #print "%s %s %s %s"%(repositorio, username, password, commit)
        result  = rpc_srv.publicarCommit(repositorio, username, password, commit)
        print result
    except:
        print "No se notifico al sistema el commit"

if __name__ == '__main__':
    cargarConfiguracion()
'''
_comandos = ['actualizar','estados','iniciar','todo']
POST_URL = "http://127.0.0.1:8000/xml_rpc_srv/"
DIR_ACTUAL = os.getcwd()

def uso():
    print __doc__

def main(argv,comando):
    '''programa principal que ejecuta a las demas funciones '''
    httpconf   = {}
    httpconf['auth'] = {}
    httpconf['mensaje'] = {}
    httpconf['repositorio'] = {}
    httpconf['path_repo']= {}
    usuario  = ''
    password = ''
    
    try:
        opts, args = getopt.getopt(argv,"hu:p:s:m:r:",["ayuda","usuario=","password=","mensaje=","repo="])
    except getopt.GetoptError:
        uso()
        sys.exit(2)
    
    if comando in _comandos:
        for opt,arg in opts:
            if opt in ("-u","--usuario"):
                httpconf['auth']['usuario'] = arg
            if opt in ("-p","--password"):
                httpconf['auth']['password'] = arg
            if opt in ("-m","--mensaje"):
                httpconf['mensaje'] = arg
            if opt in ("-r","--repositorio"):
                httpconf['repositorio'] = arg
            
        if comando == 'actualizar':
            if not(httpconf['auth'].get('usuario',None)):
                httpconf['auth']['usuario']=raw_input('Nombre de usuario:')
            if not(httpconf['auth'].get('password',None)):
                httpconf['auth']['password']=getpass('Password:')
            rpc_srv = xmlrpclib.ServerProxy(POST_URL)
            result  = rpc_srv.publicarEntrada(httpconf['auth']['usuario'],httpconf['auth']['password'],httpconf['mensaje'])
            print result
            
        if comando == 'estados':
            ''' Realizar la visualizacion de estados por repositorio '''
            if not(httpconf['auth'].get('usuario',None)):
                httpconf['auth']['usuario']=raw_input('Nombre de usuario:')
            if not(httpconf['auth'].get('password',None)):
                httpconf['auth']['password']=getpass('Password:')
            rpc_srv = xmlrpclib.ServerProxy(POST_URL)
            result = rpc_srv.estadosRepo(httpconf['auth']['usuario'],httpconf['auth']['password'], httpconf['repositorio'])
            ''' para analizar el contenido de resultado y recorrido ''' 
            try:
                print result
                xmldoc = xml.dom.minidom.parseString(result)
            
                for n in  xmldoc.childNodes :
                    print n.tagName
                    for contacto in n.childNodes:
                        for registro in contacto.childNodes:
                            if registro.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                                print "%s :%s"%(registro.nodeName,registro.firstChild.data)
                print '---'
            except:
                print result
                print "No se recibieron notificaciones."
                            
            if result == None:
                print 'Problemas con la peticion de acciones al repsoitorio'

        if comando == 'todo':
            ''' Realizar la visualizacion de todo , en general o por repositorio'''
            ''' Realizar la visualizacion de estados por repositorio '''
            if not(httpconf['auth'].get('usuario',None)):
                httpconf['auth']['usuario']=raw_input('Nombre de usuario:')
            if not(httpconf['auth'].get('password',None)):
                httpconf['auth']['password']=getpass('Password:')
            rpc_srv = xmlrpclib.ServerProxy(POST_URL)
            result = rpc_srv.todoRepo(httpconf['auth']['usuario'],httpconf['auth']['password'], httpconf['repositorio'])
            ''' para analizar el contenido de resultado y recorrido ''' 
            try:
                xmldoc = xml.dom.minidom.parseString(result)
            
                for n in  xmldoc.childNodes :
                    print n.tagName
                    for contacto in n.childNodes:
                        for registro in contacto.childNodes:
                            if registro.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                                print "%s :%s"%(registro.nodeName,registro.firstChild.data)
                print '---'
            except:
                print result
                print "No se recibieron notificaciones."
                            
            if result == None:
                print 'Problemas con la peticion de acciones al repsoitorio'


        if  comando == 'iniciar':
            configurar()
    else:
        print "publicar: '"+ comando+"' No es un comando reconocido. escribe 'publicar -h' para ver la informacion"
        sys.exit(3)
        
def configurar():
    '''metodo que verifica si el actual directorio ya esta configurado, caso contrario escribe el script
       configura y otorga el privilegio de ejecutable'''
    if Repo(DIR_ACTUAL):
        print 'directorio actual con repositorio'
    else:
        print 'directorio actual sin repo'
    post_commit = open(DIR_ACTUAL+'/.git/hooks/post-commit','wb')
    config = open(DIR_ACTUAL+'/.git/hooks/config.gme','wb')
    post_commit.write(codigo_hook)
    usuario = raw_input('Nombre de usuario para usar el repositorio:')
    password = getpass('Password de acceso al sistema:')
    config.write('{\n"repositorio":"%s",\n'%os.path.split(DIR_ACTUAL)[1])
    config.write('"username":"%s",\n'%usuario)
    config.write('"password":"%s",\n'%password)
    config.write('"pathrepo":"%s"\n}'%DIR_ACTUAL)
    dio = os.system('chmod +x %s/.git/hooks/post-commit'%DIR_ACTUAL)
    post_commit.close()
    config.close()
    print 'Se escribio el archivo de configuracion config.gme'
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Error: publicar toma por lo menos un argumento\n"
        uso()
        sys.exit(2)
    elif (len(sys.argv))==2 and sys.argv[1] in ('-h','--ayuda','ayuda'):
        uso()
        sys.exit(4)
    else:
        main(sys.argv[2:],sys.argv[1])