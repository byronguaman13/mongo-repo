# from bson import json_util
import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS,cross_origin




app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'asistenciacp',
    'host': 'mongodb+srv://asistencia_mongodb:cputn_2022@cluster0.20mqbce.mongodb.net/?retryWrites=true&w=majority',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
app.config['CORS_HEADERS'] = 'Content-Type'
cors=CORS(app)
#Rutas de la aplicación

class Reportes(db.Document):
    message = db.StringField()
    datetime = db.StringField()
    def to_json(self):
        return {"message": self.message,
                "datetime": self.datetime}

@app.route('/mongo_audit', methods=['GET'])
def query_records():

    datos = Reportes.objects()
    if not datos:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(datos)

@app.route('/mongo_audit', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    data =Reportes(message=record['message'],
                datetime=record['datetime'])
    data.save()
    return jsonify(data)

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    mensajes = {"Mensaje":"Bienvenido al api de MongoDB"}
    return mensajes

if __name__ == '__main__':
    app.run(host="0.0.0.0")
