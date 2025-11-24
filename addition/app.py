from flask import Flask, request, jsonify
import time
import redis
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Redis for tracking operations (optional - can use in-memory for demo)
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)

# Metrics
REQUEST_COUNT = Counter('addition_requests_total', 'Total addition requests')
REQUEST_LATENCY = Histogram('addition_request_latency_seconds', 'Addition request latency')
ERROR_COUNT = Counter('addition_errors_total', 'Total addition errors')


def track_operation(operation, num1, num2, result):
    """Track operation for analytics"""
    try:
        # Increment operation count
        redis_client.incr(f'operations:{operation}')

        # Store recent operations (keep last 100)
        operation_data = {
            'operation': operation,
            'num1': num1,
            'num2': num2,
            'result': result,
            'timestamp': time.time()
        }
        redis_client.lpush('recent_operations', str(operation_data))
        redis_client.ltrim('recent_operations', 0, 99)
    except:
        # Fallback if Redis is not available
        pass


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

        # Track operation
        track_operation('addition', num1, num2, result)

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


@app.route('/operations/count', methods=['GET'])
def get_operation_count():
    """Get count of operations for this service"""
    try:
        count = redis_client.get('operations:addition') or 0
        return jsonify({'operation': 'addition', 'count': int(count)})
    except:
        return jsonify({'operation': 'addition', 'count': 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)