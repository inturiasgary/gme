import unittest
from repositorio.models import *
from django.contrib.auth.models import User
from datetime import time, timedelta

class RepositorioTestCase(unittest.TestCase):
	def SetUp(self):
		self.repositorio1 = Repositorio.objects.create(nombre="repositorio1", descripcion="descripcion de repositorio",
							       direccionWeb="www.repositorio1.com", emailAdmin="repositorio1@hotmail.com",
							       )
	def testUpdateRepositorio(self):
		self.repositorio1 = Repositorio.objects.create(nombre="repositorio1", descripcion="descripcion de repositorio",
							       direccionWeb="www.repositorio1.com", emailAdmin="repositorio1@hotmail.com",
							       )
		self.repositorio1.save()
		self.repositorioPrueba = Repositorio.objects.get(nombre="repositorio1")
		self.repositorioPrueba.emailAdmin="repo@hotmail.com"
		self.repositorioPrueba.save()
		self.assertEquals(self.repositorioPrueba.emailAdmin, "repo@hotmail.com")
		
class MiembroTestCase(unittest.TestCase):
	def SetUp(self):
		self.repositorio1 = Repositorio.objects.create(nombre="repositorio1", descripcion="descripcion de repositorio",
							       direccionWeb="www.repositorio1.com", emailAdmin="repositorio1@hotmail.com",
							       )
		self.usuario1 = User.objects.create(username="usuarioPrueba")
		self.miembro = Miembro.objects.create(usuario=self.usuario1, repositorio=self.repositorio1, creador=True, activo=True)
		
	def testUpdateMiembro(self):
		self.repositorio1 = Repositorio.objects.create(nombre="repositorio12", descripcion="descripcion de repositorio",
							       direccionWeb="www.repositorio1.com", emailAdmin="repositorio1@hotmail.com",
							       )
		self.usuario1 = User.objects.create(username="usuarioPrueba2")
		self.miembro = Miembro.objects.create(usuario=self.usuario1, repositorio=self.repositorio1, creador=True, activo=True)
		self.miembroPrueba = Miembro.objects.get(usuario__username="usuarioPrueba2")
		self.miembroPrueba.activo = False
		self.miembroPrueba.save()
		self.assertEquals(self.miembroPrueba.activo, False)
