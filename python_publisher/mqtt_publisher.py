from datetime import datetime
import paho.mqtt.client as mqtt
import json, time

import random


def on_publish(client, userdata, mid):
    print("Sent a message")

mqttClient = mqtt.Client("aritra_broker_test_publisher")
mqttClient.on_publish = on_publish
mqttClient.connect('172.16.210.5', 1883)
mqttClient.loop_start()

while True:
    sensor_id = random.randint(1, 10)
    data = random.randint(1000, 9999)
    current_datetime = datetime.now()
    data = {
        "sensor_id": sensor_id,
        "data": data,
        "time": current_datetime.isoformat()
    }
    msg = json.dumps(data)  # Convert data dictionary to JSON string
    info = mqttClient.publish(
        topic='python/test',
        payload=msg,  # No need to encode as 'utf-8' since it's already a JSON string
        qos=0,
    )
    info.wait_for_publish()
    print(f"Published: {msg}")
    time.sleep(3)
