from datetime import datetime
import paho.mqtt_client.client as mqtt_client
import json, time
import random
from environ import environ

class envData:
    env = environ.Env()
    environ.Env.read_env()
    MOSQUITTO_BROKER_IP = env('MOSQUITTO_BROKER_IP')
    MOSQUITTO_BROKER_PORT = env('MOSQUITTO_BROKER_PORT')
    MOSQUITTO_BROKER_TOPIC = env('MOSQUITTO_BROKER_TOPIC')

def on_publish(client, userdata, mid):
    print("Sent a message")

client = mqtt_client.Client("mqtt_publisher")
client.on_publish = on_publish
client.connect(envData.MOSQUITTO_BROKER_IP, int(envData.MOSQUITTO_BROKER_PORT))
client.loop_start()

while True:
    sensor_id = random.randint(1, 10)
    data = random.randint(1000, 9999)
    current_datetime = datetime.now()
    data = {
        "sensor_id": sensor_id,
        "data": data,
        "time": current_datetime.isoformat()
    }
    msg = json.dumps(data)
    info = client.publish(
        topic='python/test',
        payload=msg,  # No need to encode as 'utf-8' since it's already a JSON string
        qos=0,
    )
    info.wait_for_publish()
    print(f"Published: {msg}")
    time.sleep(3)
