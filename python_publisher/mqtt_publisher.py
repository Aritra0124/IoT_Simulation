from datetime import datetime
import paho.mqtt.client as mqtt_client
import json, time
import random
from environ import environ


class EnvData:
    env = environ.Env()
    environ.Env.read_env()
    MOSQUITTO_BROKER_IP = env('MOSQUITTO_BROKER_IP')
    MOSQUITTO_BROKER_PORT = int(env('MOSQUITTO_BROKER_PORT'))
    MOSQUITTO_BROKER_TOPIC = env('MOSQUITTO_BROKER_TOPIC')


def random_data():
    sensor_id = random.randint(1, 10)
    data = random.randint(1000, 9999)
    current_datetime = datetime.now()
    data = {
        "sensor_id": sensor_id,
        "data": data,
        "time": current_datetime.isoformat()
    }
    msg = json.dumps(data)
    return msg


def on_publish(client, userdata, mid):
    print("Sent a message")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection to MQTT broker failed with code {rc}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        client.reconnect()


def run():
    client = mqtt_client.Client("mqtt_publisher")
    client.on_connect = on_connect
    client.on_publish = on_publish

    while True:
        try:
            client.connect(EnvData.MOSQUITTO_BROKER_IP, EnvData.MOSQUITTO_BROKER_PORT)
            client.loop_start()

            payload = random_data()
            info = client.publish(
                topic=EnvData.MOSQUITTO_BROKER_TOPIC,
                payload=payload,
                qos=0,
            )
            info.wait_for_publish()
            print(f"Published: {payload}")

            client.disconnect()
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(3)


if __name__ == '__main__':
    run()
