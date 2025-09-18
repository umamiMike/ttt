import paho.mqtt.client as mqtt
from web.session import Session
from core.game import WrongTurn, WrongFirst
import json
import uuid

BROKER = "localhost"
TOPIC_MOVES = "game/move"
TOPIC_STATE = "game/state"


class BackendClient(mqtt.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = Session()
        super().__init__()

        self.connect(BROKER, 1883, 60)
        # self.on_connect = on_connect
        # self.on_message = on_message

    def on_connect(self, userdata, flags, rc, properties=None):
        print("Connected with result code", rc)
        self.subscribe(TOPIC_MOVES)

    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode())

        match message["action"]:
            case "browser_connect":
                print("conn")
            case "join":
                self.handle_join(**message["data"])
            case "take_turn":
                self.handle_turn(**message["data"])

            case _:
                print(message["action"])

    def handle_join(self, name):
        joined = self.session.join(name)
        if joined:
            self.publish(
                TOPIC_STATE,
                json.dumps({"state": str(joined), "data": {"player": name}}),
            )
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {
                        "state": "started",
                        "data": {"board_state": self.session.game.board_data()},
                    }
                ),
            )

    def handle_turn(self, player, cell):
        try:
            board_state, player = self.session.take_turn(player, cell)
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {
                        "state": "turn_taken",
                        "data": {
                            "board_state": self.session.game.board_data(),
                            "player": player,
                        },
                    }
                ),
            )
        except WrongFirst as e:
            json.dumps(
                {
                    "state": "no_turn",
                    "data": {
                        "board_state": self.session.game.board_data(),
                        "player": player,
                    },
                }
            )
        except WrongTurn as e:
            print("should log this error")
            json.dumps(
                {
                    "state": "no_turn",
                    "data": {
                        "board_state": self.session.game.board_data(),
                        "player": player,
                    },
                }
            )


backend = BackendClient(mqtt.CallbackAPIVersion.VERSION2, client_id="backend_client")
backend.loop_forever()
