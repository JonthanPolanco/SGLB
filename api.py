from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import uuid

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://jona332:than233@cluster0.gvzqbpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)


class Ruta:
    def __init__(self, nombre, origen, destino):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.origen = origen
        self.destino = destino


class Buseta:
    def __init__(self, numero, conductor, capacidad):
        self.id = str(uuid.uuid4())
        self.numero = numero
        self.conductor = conductor
        self.capacidad = capacidad


@app.route('/rutas', methods=['GET'])
def obtener_rutas():
    rutas = mongo.db.rutas.find()
    resultados = []
    for ruta in rutas:
        ruta_data = {'id': ruta['_id'], 'nombre': ruta['nombre'], 'origen': ruta['origen'], 'destino': ruta['destino']}
        resultados.append(ruta_data)
    return jsonify(resultados)


@app.route('/rutas', methods=['POST'])
def crear_ruta():
    datos = request.get_json()
    nombre = datos['nombre']
    origen = datos['origen']
    destino = datos['destino']
    nueva_ruta = Ruta(nombre, origen, destino)
    ruta = {'_id': nueva_ruta.id, 'nombre': nueva_ruta.nombre, 'origen': nueva_ruta.origen, 'destino': nueva_ruta.destino}
    mongo.db.rutas.insert_one(ruta)
    return jsonify({'mensaje': 'Ruta creada exitosamente', 'id': nueva_ruta.id})


@app.route('/rutas/<ruta_id>', methods=['GET'])
def obtener_ruta(ruta_id):
    ruta = mongo.db.rutas.find_one({'_id': ruta_id})
    if ruta:
        ruta_data = {'id': ruta['_id'], 'nombre': ruta['nombre'], 'origen': ruta['origen'], 'destino': ruta['destino']}
        return jsonify(ruta_data)
    else:
        return jsonify({'mensaje': 'Ruta no encontrada'}), 404


@app.route('/rutas/<ruta_id>', methods=['PUT'])
def actualizar_ruta(ruta_id):
    ruta = mongo.db.rutas.find_one({'_id': ruta_id})
    if ruta:
        datos = request.get_json()
        ruta['nombre'] = datos['nombre']
        ruta['origen'] = datos['origen']
        ruta['destino'] = datos['destino']
        mongo.db.rutas.update_one({'_id': ruta_id}, {'$set': ruta})
        return jsonify({'mensaje': 'Ruta actualizada exitosamente'})
    else:
        return jsonify({'mensaje': 'Ruta no encontrada'}), 404


@app.route('/rutas/<ruta_id>', methods=['DELETE'])
def eliminar_ruta(ruta_id):
    ruta = mongo.db.rutas.find_one({'_id': ruta_id})
    if ruta:
        mongo.db.rutas.delete_one({'_id': ruta_id})
        return jsonify({'mensaje': 'Ruta eliminada exitosamente'})
    else:
        return jsonify({'mensaje': 'Ruta no encontrada'}), 404
