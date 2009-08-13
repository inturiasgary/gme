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
		self.assertEquals( self.assertEqual(self.repositorioPrueba.emailAdmin, "repo@hotmail.com"))
