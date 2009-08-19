import unittest
from models import Cuenta
from django.contrib.auth.models import User
from django.conf import settings

class CuentaTestCase(unittest.TestCase):
    def SetUp(self):
        usuario = User(username="userDemo")
        usuario.set_password("userDemo")
        usuario.save()
        self.cuenta1 = Cuenta.objects.create(user=usuario)