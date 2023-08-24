import paho.mqtt.client as mqtt_client
import json
import db_save

broker = '172.16.210.5'
port = 1883
topic = "python/test"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)  # Subscribe to the topic upon successful connection
        else:
            print("Failed to connect, return code", rc)

    client = mqtt_client.Client("aritra_broker_test_subscriber")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    payload = msg.payload.decode()  # Convert payload to a string
    data = json.loads(payload)  # Parse the JSON payload
    print(f"Received data: {data}")
    db_save.save_data(data)
def run():
    client = connect_mqtt()
    client.on_message = on_message  # Assign on_message callback
    client.loop_forever()

if __name__ == '__main__':
    run()
