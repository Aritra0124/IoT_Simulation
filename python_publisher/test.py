import paho.mqtt.publish as publish

k = publish.single("test", "HelloWorld", hostname="172.16.210.5", port=8883)
print(k)