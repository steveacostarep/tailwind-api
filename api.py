from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar CORS
import json

app = Flask(__name__)
CORS(app)  # Habilitar CORS para la aplicación

# Cargar la información desde el archivo JSON
with open("documentacion_tailwind.json", "r", encoding="utf-8") as f:
    documentacion = json.load(f)["contenido"]  # Extraer solo el contenido

# Ruta para obtener toda la documentación
@app.route('/documentacion', methods=['GET'])
def obtener_documentacion():
    return jsonify({"contenido": documentacion})

# Ruta para buscar por un fragmento de texto en el contenido de la documentación
@app.route('/buscar', methods=['GET'])
def buscar_contenido():
    query = request.args.get('q', '').lower()
    
    if query:
        if query in documentacion.lower():
            return jsonify({"resultado": query})
        else:
            return jsonify({"error": "No se encontraron resultados"}), 404
    else:
        return jsonify({"error": "No se proporcionó una consulta"}), 400

if __name__ == '__main__':
    # Configuración para Railway, obtener el puerto de la variable de entorno
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
