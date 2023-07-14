from flask import Flask, request, jsonify
from datetime import datetime
from models import *

app = Flask(__name__)

@app.route("/billetera/contactos", methods=["GET"])
def obtener_contactos():
    numero = request.args.get("minumero")
    cuenta = get_cuenta(numero)
    if cuenta is None:
        return jsonify({
            "message": "Cuenta no encontrada"
        }), 404
    
    contactos = {}
    for contacto in cuenta.contactos:
        potential_contact = get_cuenta(contacto).nombre
        if potential_contact is None:
            contactos[contacto] = "Desconocido"
        else:
            contactos[contacto] = potential_contact

    return jsonify(contactos), 200

@app.route("/billetera/pagar", methods=["GET"])
def realizar_pago():
    numero = request.args.get("minumero")
    destino = request.args.get("numerodestino")
    valor = float(request.args.get("valor"))

    cuenta = get_cuenta(numero)
    if cuenta is None:
        return jsonify({
            "message": "Cuenta no encontrada"
        }), 404

    res = cuenta.pagar(destino, valor)
    if res != "Pago realizado.":
        return jsonify({
            "message": res
        }), 400
    
    today = datetime.now().strftime('%d/%m/%Y')

    return jsonify({
        "message": f"Realizado en {today}"
    }), 200

@app.route("/billetera/historial", methods=["GET"])
def obtener_historial():
    numero = request.args.get("minumero")
    cuenta = get_cuenta(numero)
    if cuenta is None:
        return jsonify({
            "message": "Cuenta no encontrada."
        }), 404

    return jsonify({
        "historial": cuenta.historial()
    }), 200

if __name__ == "__main__":
    app.run()
