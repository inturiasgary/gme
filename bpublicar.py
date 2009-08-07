#!/usr/bin/env python
'''publicar es un CLI simple para la publicacion de estados al microblog GME global.

Uso: publicar comando [opciones]

Comando:

 actualizar    Actualiza tu mensaje de estado en el sistema microblog global
 estados       Muestra todos los 10 estados ultimos publicados de tus amigos
 
Opciones:

 -u, --usuario            Nombre de usuario
 -p, --password           Password
 -m, --mensaje            Mensaje
 -r, --repositorio        Repositorio
'''
import sys
import getopt
import xmlrpclib

_comandos = ['actualizar','estados']

def uso():
    print __doc__

def main(argv,comando):
    httpconf   = {}
    httpconf['auth'] = {}
    httpconf['mensaje'] = {}
    httpconf['repositorio'] = {}
    usuario  = 'gary'
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
                from getpass import getpass
                httpconf['auth']['password']=getpass('Password:')
            rpc_srv = xmlrpclib.ServerProxy("http://127.0.0.1:8000/xml_rpc_srv/")
            result  = rpc_srv.publicarEntrada(httpconf['auth']['usuario'],httpconf['auth']['password'],httpconf['mensaje'])
            print result
    else:
        print "publicar: '"+ comando+"' No es un comando reconocido. escribe 'publicar -h' para ver la informacion"
        sys.exit(3)
    
    
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