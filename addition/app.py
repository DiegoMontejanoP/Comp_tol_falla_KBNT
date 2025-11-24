from flask import Flask, request, jsonify
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('addition_requests_total', 'Total addition requests')
REQUEST_LATENCY = Histogram('addition_request_latency_seconds', 'Addition request latency')
ERROR_COUNT = Counter('addition_errors_total', 'Total addition errors')


@app.route('/calculate', methods=['POST'])
def calculate():
    start_time = time.time()
    REQUEST_COUNT.inc()

    data = request.json
    try:
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        result = num1 + num2

        # Record latency
        REQUEST_LATENCY.observe(time.time() - start_time)

        return jsonify({'result': result, 'operation': 'addition'})
    except (ValueError, KeyError) as e:
        ERROR_COUNT.inc()
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'addition'})


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)