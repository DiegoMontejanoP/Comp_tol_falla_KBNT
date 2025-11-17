from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# URLs de los servicios (usaremos nombres de servicio Kubernetes)
SERVICIOS = {
    'suma': f"http://{os.getenv('SUMA_SERVICE', 'servicio-suma')}:5000/sumar",
    'resta': f"http://{os.getenv('RESTA_SERVICE', 'servicio-resta')}:5000/restar",
    'multiplicacion': f"http://{os.getenv('MULTIPLICACION_SERVICE', 'servicio-multiplicacion')}:5000/multiplicar",
    'division': f"http://{os.getenv('DIVISION_SERVICE', 'servicio-division')}:5000/dividir",
    'exponente': f"http://{os.getenv('EXPONENTE_SERVICE', 'servicio-exponente')}:5000/exponenciar"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.json
        operacion = data.get('operacion')
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))

        servicio_url = SERVICIOS.get(operacion)

        if not servicio_url:
            return jsonify({'error': 'Operación no válida'}), 400

        # Llamar al servicio correspondiente
        response = requests.post(servicio_url, json={'a': a, 'b': b}, timeout=5)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Error en el servicio'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)