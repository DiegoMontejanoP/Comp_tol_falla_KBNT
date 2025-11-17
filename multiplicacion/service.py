from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

@app.route('/multiplicar', methods=['POST'])
def multiplicar():
    try:
        data = request.json
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))

        # Simular procesamiento más complejo
        time.sleep(random.uniform(0.2, 0.8))

        resultado = a * b
        return jsonify({
            'operacion': 'multiplicacion',
            'resultado': resultado,
            'detalles': f'{a} × {b} = {resultado}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'servicio': 'multiplicacion'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)