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
        minumero = "21345"
        numerodestino = "123"
        valor = "75"
        response = self.client().get(f'/billetera/pagar?minumero={minumero}&numerodestino={numerodestino}&valor={valor}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], f"Realizado en {self.today}.")

    def test_pago_cuenta_no_encontrada(self):
        minumero = "000"
        numerodestino = "123"
        valor = "75"
        response = self.client().get(f'/billetera/pagar?minumero={minumero}&numerodestino={numerodestino}&valor={valor}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Cuenta no encontrada.") 

    def test_historial_cuenta_no_encontrada(self):
        minumero = "000"
        response = self.client().get(f'/billetera/historial?minumero={minumero}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Cuenta no encontrada.")

    def test_pago_saldo_insuficiente(self):
        minumero = "21345"
        numerodestino = "123"
        valor = "1000"
        response = self.client().get(f'/billetera/pagar?minumero={minumero}&numerodestino={numerodestino}&valor={valor}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Saldo insuficiente.")

#python -m unittest tests