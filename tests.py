from datetime import datetime
import unittest
from app import app
import json

class TestBilletera(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.today = datetime.now().strftime('%d/%m/%Y')

    def test_pago_exito(self):
        minumero = "21345" #usuario real
        numerodestino = "123" #usuario real y en contactos
        valor = "75" #valor de acuerdo al saldo
        response = self.client().get(f'/billetera/pagar?minumero={minumero}&numerodestino={numerodestino}&valor={valor}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200) #código de éxito
        self.assertEqual(data["message"], f"Realizado en {self.today}.") #mensaje de éxito

    def test_pago_contacto_no_encontrado(self):
        minumero = "123" #usuario real
        numerodestino = "21345" #usuario real NO en contactos
        valor = "75" #valor de acuerdo al saldo
        response = self.client().get(f'/billetera/pagar?minumero={minumero}&numerodestino={numerodestino}&valor={valor}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400) #código de error 400 (solicitud incorrecta)
        self.assertEqual(data["message"], "El número de destino no está en los contactos.") #mensaje de error

    def test_pago_saldo_insuficiente(self):
        minumero = "21345" #usuario real
        numerodestino = "123" #usuario real y en contactos
        valor = "1000" #valor mayor al saldo
        response = self.client().get(f'/billetera/pagar?minumero={minumero}&numerodestino={numerodestino}&valor={valor}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400) #código de error 400 (solicitud incorrecta)
        self.assertEqual(data["message"], "Saldo insuficiente.") #mensaje de error
    
    def test_historial_cuenta_no_encontrada(self):
        minumero = "000" #usuario no existente
        response = self.client().get(f'/billetera/historial?minumero={minumero}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404) #código de error 404 (no encontrado)
        self.assertEqual(data["message"], "Cuenta no encontrada.") #mensaje de error

#python -m unittest tests