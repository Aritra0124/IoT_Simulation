import paho.mqtt.client as mqtt_client
import json, time, os, redis
import db_save

# This class used to access env variables.
class envData:
    MOSQUITTO_BROKER_IP = os.getenv('MOSQUITTO_BROKER_IP')
    MOSQUITTO_BROKER_PORT = os.getenv('MOSQUITTO_BROKER_PORT')
    MOSQUITTO_BROKER_TOPIC = os.getenv('MOSQUITTO_BROKER_TOPIC')


# To connect with redisdb
redis_client = redis.StrictRedis(host='redis_db', port=6379, db=0, decode_responses=True)

# This section is used to create MQTT subscriber.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(envData.MOSQUITTO_BROKER_TOPIC)
    else:
        print("Connection to MQTT broker failed. Retrying in 5 seconds...")
        time.sleep(5)
        client.reconnect()

def on_message(client, userdata, msg):

    payload = msg.payload.decode()
    try:
        data = payload

        # Insert the oldest data into redis
        redis_client.rpush("sensor_data", data)

        # Check list length is greater than 10 or not
        if redis_client.llen('sensor_data') > 10:

            # Pop the oldest data from list
            oldest_data = json.loads(redis_client.lpop('sensor_data'))

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
