from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import time

app = Flask(__name__)

ARCHIVO = os.path.join(os.path.dirname(__file__), "peritajes.json")

inventario = {
    "servidor": "Servidor-Daza",
    "hora_servidor": str(datetime.now()),
    "motos": [
        {
            "placa": "JPD087",
            "modelo": "Yamaha R15"
        },
        {
            "placa": "BBB222",
            "modelo": "Pulsar NS200"
        }
    ]
}

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w") as f:
        json.dump([], f)

@app.route('/api/registros', methods=['GET'])
def registros():
    return jsonify(inventario)

@app.route('/api/peritajes', methods=['POST'])
def agregar_peritaje():

    datos = request.json
    for clave in datos:
        if isinstance(datos[clave], str):
            datos[clave] = datos[clave].upper()

    with open(ARCHIVO, "r") as f:
        peritajes = json.load(f)

    peritajes.append(datos)

    with open(ARCHIVO, "w") as f:
        json.dump(peritajes, f, indent=4)

    return jsonify({
        "mensaje": "Moto registrada correctamente",
        "datos": datos
    }), 201

@app.route('/api/peritajes', methods=['GET'])
def obtener_peritajes():

    with open(ARCHIVO, "r") as f:
        peritajes = json.load(f)

    return jsonify(peritajes)

@app.route('/api/peritajes/<placa>', methods=['DELETE'])
def eliminar_peritaje(placa):

    with open(ARCHIVO, "r") as f:
        peritajes = json.load(f)

    nueva_lista = []
    moto_eliminada = None

    for moto in peritajes:
        if moto["placa"] == placa:
            moto_eliminada = moto
        else:
            nueva_lista.append(moto)

    with open(ARCHIVO, "w") as f:
        json.dump(nueva_lista, f, indent=4)

    return jsonify({
        "message": f"Vehículo {placa} entregado al cliente con éxito",
        "moto_removida": moto_eliminada
    })

@app.route('/api/inventario')
def inventario_api():
    return jsonify({
        "repuestos": [
            "Aceite",
            "Pastillas de freno",
            "Llantas",
            "Bateria"
        ]
    })


@app.route('/api/health', methods=['GET'])
def health_check():

    sistema_archivos_ok = os.path.exists('/tmp') or os.path.exists('.')

    if sistema_archivos_ok:
        return jsonify({
            "status": "healthy",
            "timestamp": int(time.time()),
            "environment": "production-cloud",
            "uptime_check": "passed"
        }), 200

    else:
        return jsonify({
            "status": "unhealthy",
            "reason": "Storage unreachable"
        }), 500    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
