from flask import Flask
import redis
import random
import json

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, db=0)  # Ajusta según tu configuración

@app.route('/health', methods=['GET'])
def health_check():
    status = random.choice(['up', 'down'])
    message = json.dumps({'service': 'plan_deportivo', 'status': status})
    redis_client.publish('health_checks', message)
    return "Health status updated"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
