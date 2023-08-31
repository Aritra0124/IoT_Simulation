import paho.mqtt.client as mqtt_client
import db_save
import json
import redis

# MQTT broker configuration
broker = '172.16.210.5'
port = 1883
topic = "python/test"

# Redis configuration
redis_host = 'redis_db'
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


latest_data = []


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client("mqtt_subscriber")
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    global latest_data

    payload = msg.payload.decode()
    data = json.loads(payload)

    latest_data.append(data)
    if len(latest_data) > 10:
        oldest_data = latest_data.pop(0)
        redis_client.lpush("latest_data_list", json.dumps(oldest_data))

        # Insert the oldest data into MongoDB
        db_save.save_data(oldest_data)
    print("Received data:", data)


def run():
    client = connect_mqtt()
    client.on_message = on_message
    client.subscribe(topic)
    client.loop_forever()


if __name__ == '__main__':
    run()
