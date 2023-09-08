import paho.mqtt.client as mqtt_client
import db_save
import json
import redis
from environ import environ
import time

class envData:
    env = environ.Env()
    environ.Env.read_env()
    MOSQUITTO_BROKER_IP = env('MOSQUITTO_BROKER_IP')
    MOSQUITTO_BROKER_PORT = env('MOSQUITTO_BROKER_PORT')
    MOSQUITTO_BROKER_TOPIC = env('MOSQUITTO_BROKER_TOPIC')

redis_client = redis.StrictRedis(host='redis_db', port=6379, db=0)

latest_data = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(envData.MOSQUITTO_BROKER_TOPIC)
    else:
        print("Connection to MQTT broker failed. Retrying in 5 seconds...")
        time.sleep(5)
        client.reconnect()

def on_message(client, userdata, msg):
    global latest_data

    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        latest_data.append(data)

        if len(latest_data) > 10:
            oldest_data = latest_data.pop(0)
            redis_client.lpush("latest_data_list", json.dumps(oldest_data))

            # Insert the oldest data into MongoDB
            db_save.save_data(oldest_data)
        print("Received data:", data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON data: {e}")

def connect_mqtt() -> mqtt_client:
    while True:
        try:
            client = mqtt_client.Client("mqtt_subscriber")
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(envData.MOSQUITTO_BROKER_IP, int(envData.MOSQUITTO_BROKER_PORT))
            return client
        except ConnectionRefusedError as e:
            print(f"Failed to connect to MQTT broker: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

def run():
    while True:
        client = connect_mqtt()
        client.loop_forever()

if __name__ == '__main__':
    run()
