from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)


@app.route('/sumar', methods=['POST'])
def sumar():
    try:
        data = request.json
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))

        # Simular procesamiento variable
        time.sleep(random.uniform(0.1, 0.5))

        resultado = a + b
        return jsonify({
            'operacion': 'suma',
            'resultado': resultado,
            'detalles': f'{a} + {b} = {resultado}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'servicio': 'suma'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)