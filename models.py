from datetime import datetime

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = []

    def historial(self):
        historial = f"Saldo de {self.nombre}: {self.saldo}\n"
        historial += f"Operaciones de {self.nombre}\n"
        for operacion in self.operaciones:
            historial += operacion.__str__() + "\n"
        return historial

    def pagar(self, num_destino, valor):
        if num_destino not in self.contactos:
            return "El número de destino no es válido."
        if self.saldo < valor:
            return "Saldo insuficiente."
        cuenta_destino = get_cuenta(num_destino)
        if cuenta_destino is None:
            return "Cuenta destino no encontrada."   
        
        self.saldo -= valor
        realizada = Operacion(num_destino, self.numero, valor, "realizado")
        recibida = Operacion(num_destino, self.numero, valor, "recibido")
        self.operaciones.append(realizada)
        cuenta_destino.operaciones.append(recibida)

        return "Pago realizado."


class Operacion:
    def __init__(self, numero_destino, numero_origen, valor, tipo):
        self.numero_destino = numero_destino
        self.numero_origen = numero_origen
        self.fecha = datetime.now().strftime('%d/%m/%Y')
        self.valor = valor
        self.tipo = tipo
    
    def __str__(self):
        if self.tipo == "recibido":
            return f"Pago {self.tipo} de {self.valor} de {self.numero_origen}"
        elif self.tipo == "realizado":
            return f"Pago {self.tipo} de {self.valor} a {self.numero_destino}"

BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

def get_cuenta(numero):
    for cuenta in BD:
        if cuenta.numero == numero:
            return cuenta
    return None
