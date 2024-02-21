import redis
import sqlite3
import json

redis_client = redis.Redis(host='redis', port=6379, db=0)

conn = sqlite3.connect('monitoring.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS service_status
             (service_name TEXT, status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def handle_message(message):
    data = json.loads(message['data'])
    service_name = data['service']
    status = data['status']
    
    c.execute("INSERT INTO service_status (service_name, status) VALUES (?, ?)", (service_name, status))
    conn.commit()
    
    print(f"Monitored {service_name}, status: {status}")

def listen_for_health_checks():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(**{'health_checks': handle_message})
    print("Starting to listen on 'health_checks' channel...")
    pubsub.run_in_thread(sleep_time=0.001)

if __name__ == '__main__':
    listen_for_health_checks()
