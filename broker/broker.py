import paho.mqtt.client as mqtt
from web.session import Session
import json

BROKER = "localhost"
TOPIC_MOVES = "game/move"
TOPIC_STATE = "game/state"

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_STATE)
    client.subscribe(TOPIC_MOVES)

def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode())
    print(message)

    if message["action"] == "connect":
        breakpoint()
    if message["action"] == "take_turn":
        breakpoint()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="player_1",)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)


client.loop_forever()
