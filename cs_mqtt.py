from paho.mqtt import client as mqtt_client
import time

broker = '192.168.1.45'
port = 1883
topic = "/curemsenes/eink"
client_id = "eink"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = "msg"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send "+msg)
        else:
            print("Failed to send message to topic")
        msg_count += 1


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("Received "+msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def thread_mqtt(inicio):
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

