from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        num1 = float(data['num1'])
        num2 = float(data['num2'])

        if num2 == 0:
            return jsonify({'error': 'Division by zero is not allowed'}), 400

        result = num1 / num2
        return jsonify({'result': result, 'operation': 'division'})
    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'division'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)