from flask import Flask
import redis
import random
import json

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, db=0)

@app.route('/health', methods=['POST'])
def health_check():
    if random.randint(1, 100) <= 10:
        status = 'down'
    else:
        status = 'up'
    
    message = json.dumps({'service': 'deportistas', 'status': status})
    redis_client.publish('health_checks', message)
    return "Health status updated"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
