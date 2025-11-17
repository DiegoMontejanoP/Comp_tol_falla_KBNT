from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)


@app.route('/dividir', methods=['POST'])
def dividir():
    try:
        data = request.json
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))

        if b == 0:
            return jsonify({'error': 'División por cero no permitida'}), 400

        # Simular procesamiento con validación
        time.sleep(random.uniform(0.1, 0.4))

        resultado = a / b
        return jsonify({
            'operacion': 'division',
            'resultado': resultado,
            'detalles': f'{a} ÷ {b} = {resultado}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'servicio': 'division'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)