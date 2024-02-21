from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/<service>/<action>', methods=['GET', 'POST'])
def gateway(service, action):
    if request.method == 'POST':
        data = request.json
        response = requests.post(f'http://{service}:5000/{action}', json=data)
        return response.content
    else:
        response = requests.get(f'http://{service}:5000/{action}')
        return response.content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
