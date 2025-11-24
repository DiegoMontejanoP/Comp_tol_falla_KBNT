from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Service URLs (will be set via environment variables in Kubernetes)
ADDITION_SERVICE = os.getenv('ADDITION_SERVICE', 'http://localhost:5001')
SUBTRACTION_SERVICE = os.getenv('SUBTRACTION_SERVICE', 'http://localhost:5002')
MULTIPLICATION_SERVICE = os.getenv('MULTIPLICATION_SERVICE', 'http://localhost:5003')
DIVISION_SERVICE = os.getenv('DIVISION_SERVICE', 'http://localhost:5004')


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kubernetes Calculator</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .calculator { max-width: 300px; margin: 0 auto; }
            input, select, button { 
                width: 100%; 
                padding: 10px; 
                margin: 5px 0; 
                font-size: 16px; 
            }
            .result { 
                margin-top: 20px; 
                padding: 10px; 
                background: #f0f0f0; 
                border-radius: 5px; 
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <h2>Kubernetes Calculator</h2>
            <input type="number" id="num1" placeholder="First number" step="any" required>
            <input type="number" id="num2" placeholder="Second number" step="any" required>
            <select id="operation">
                <option value="add">Addition (+)</option>
                <option value="subtract">Subtraction (-)</option>
                <option value="multiply">Multiplication (*)</option>
                <option value="divide">Division (/)</option>
            </select>
            <button onclick="calculate()">Calculate</button>
            <div id="result" class="result"></div>
        </div>

        <script>
            async function calculate() {
                const num1 = parseFloat(document.getElementById('num1').value);
                const num2 = parseFloat(document.getElementById('num2').value);
                const operation = document.getElementById('operation').value;

                if (isNaN(num1) || isNaN(num2)) {
                    alert('Please enter valid numbers');
                    return;
                }

                try {
                    const response = await fetch('/calculate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            num1: num1,
                            num2: num2,
                            operation: operation
                        })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('result').innerHTML = 
                            `<strong>Result:</strong> ${data.result}`;
                    } else {
                        document.getElementById('result').innerHTML = 
                            `<strong>Error:</strong> ${data.error}`;
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 
                        `<strong>Error:</strong> Service unavailable`;
                }
            }
        </script>
    </body>
    </html>
    '''


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    num1 = data['num1']
    num2 = data['num2']
    operation = data['operation']

    service_urls = {
        'add': ADDITION_SERVICE,
        'subtract': SUBTRACTION_SERVICE,
        'multiply': MULTIPLICATION_SERVICE,
        'divide': DIVISION_SERVICE
    }

    service_url = service_urls.get(operation)
    if not service_url:
        return jsonify({'error': 'Invalid operation'}), 400

    try:
        response = requests.post(f"{service_url}/calculate",
                                 json={'num1': num1, 'num2': num2},
                                 timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Service unavailable: {str(e)}'}), 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)