#!/usr/bin/env python
import os, sys, shutil, shelve
import urlib, urlib2

try:
	from git import *
except:
	print "no se encuentr gitPython favor instalelo"
DIR_ACTUAL = os.getcwd() #para obtener el directorio actual de trabajo
print "Repositorio actual de trabajo: %s"%DIR_ACTUAL
try:
	repo = Repo(DIR_ACTUAL)
	print "Repositorio actual con git"
	pcommit = "post-commit"
	configuracion = shelve.open('config')
	informacion = []
	informacion.append(nombre)
	informacion.append(contrasena)
	if configurar():
		while(nombre.length()==0 or contrasena.length()==0):
			#Falta hacer la validacion directocon el server de la web
			nombre = raw_input("Favor introduzca su login: ")
			contrasena = raw_input("Favor introduzca su password: ")
		FILE = open(os.path.join(DIR_ACTUAL,'/.git/hooks/conf',"w"))
		FILE.write("nombre del repositorio: %s\nlogin: %s\npassword:%s"%(nombreRepositorio, nombre, contrasena))
		FILE.close()
except:
	print "El directorio actual no es un repositorio subversionado con git"
	respuesta = raw_input("Desea inicialiar un repositorio?(s/n): ")
	if respuesta == 's' or respuesta == 'S':
		repo = Repo.init_bare(DIR_ACTUAL)
	else:
		print 'Operacion Abortada'
		break

def verificarConfiguracion():
	''' Verificar el estado actual del archivo de configuracion '''
	conf = os.path.join(DIR_ACTUAL, '/.git/hooks/conf')
	if conf:
		res = raw_input('Actualmente se encuentra configurado, desea sobreescribir?(s/n):')
	else:
		print 'Se aborto la configuracion, se deja configurado el conf'
		break
	else:
		return true
	return false

def verificarRepo():
	''' Si es repositorio en la web, se une como miembro'''
	''' Caso contrario lo crea, y se une '''
	res = raw_input('Repositorio aun no creado en la web, desea crearlos?(s/n)')
	resultado = verificarRespuesta(res)
	if res:
		print 'verificamos'
	else:
		print 'no acaba aun'

def verificarRespuesta(res):
	if res='s' or res='S':
		return True
	else:
		if res=='n' or res=='N':
			return False
	print 'Respuesta no esperada, operacion abortada'
	break
