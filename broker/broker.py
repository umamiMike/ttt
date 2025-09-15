import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC_MOVES = "game/move"
TOPIC_STATE = "game/state"

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_STATE)

def on_message(client, userdata, msg):
    print("State update:", msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="player_1",)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)


client.loop_forever()
