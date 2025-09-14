import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC_MOVES = "game/move"
TOPIC_STATE = "game/state"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_STATE)

def on_message(client, userdata, msg):
    print("State update:", msg.payload.decode())

client = mqtt.Client(callback_api_version=2)
client.username_pw_set("u", "p")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)

client.loop_start()

# Send a move
client.publish(TOPIC_MOVES, "terminal: X at (0,0)")

