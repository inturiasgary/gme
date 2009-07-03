#!/usr/bin/env python
# encoding: utf-8 
import sys      #importamos la libreria sys
import string       #para hacer el uso de juntar todas las letras
if sys.argv[1]=="m":
    print "Se soguio el rumbo"
else:
    print "Comando no invalido"
    pass
commit = string.join(sys.argv[2:])       #capturamos la información
print "Mensaje capturado: "+commit
