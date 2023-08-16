import requests
from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/receive_message', methods=['POST'])
def receive_message():
    data = request.get_json()  # Obtener los datos del POST como JSON

    # Suponiendo que los tres parámetros son 'param1', 'param2' y 'param3'

    rutina = {
        "nombre": "Lobo",
        "ejercicios": [
            {
            "nombre": "Flexiones",
            "series": 3,
            "numero_ejercicios": 10
            },
            {
            "nombre": "Sentadillas",
            "series": 4,
            "numero_ejercicios": 12
            },
            {
            "nombre": "Abdominales",
            "series": 3,
            "numero_ejercicios": 15
            },
            {
            "nombre": "Burpees",
            "series": 2,
            "numero_ejercicios": 8
            }
        ]
    }

    rutina = data.get('rutina')
    ejercicios = data.get('ejercicios')
    series = data.get('series')

    # Aquí puedes realizar cualquier acción con los parámetros recibidos

    response = {'message': 'Message received successfully'}
    return jsonify(response)
