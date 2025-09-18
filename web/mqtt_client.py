import paho.mqtt.client as mqtt
from web.session import Session
from core.game import WrongTurn, WrongFirst, GameOver
import json
import uuid

BROKER = "localhost"
TOPIC_MOVES = "game/move"
TOPIC_STATE = "game/state"


class BackendClient(mqtt.Client):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.session = Session()

        self.connect(BROKER, 1883, 60)

    def on_connect(self, userdata, flags, rc, properties=None):
        print("Connected with result code", rc)
        self.subscribe(TOPIC_MOVES)

    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode())
        print("incoming message: ", message)
        match message["action"]:
            case "browser_connect":
                self.handle_conn(**message["data"])
            case "join":
                self.handle_join(**message["data"])
            case "take_turn":
                self.handle_turn(**message["data"])
            case "reset":
                self.handle_reset()
            case _:
                print(message["action"])

    def handle_conn(self, msg):
        self.publish(
            TOPIC_STATE,
            json.dumps(
                {"state": "connected", "data": {"players": self.session.players_data()}}
            ),
        )

    def handle_reset(self):
        self.session.new_game()
        self.publish(
            TOPIC_STATE,
            json.dumps(
                {
                    "state": "reset",
                    "data": {"players": self.session.players_data()},
                    "board_state": self.session.game.board_data(),
                }
            ),
        )

    def handle_join(self, name):

        # full
        if len(self.session.players) == 2:
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {"state": "full", "data": {"players": self.session.players_data()}}
                ),
            )

        self.session.join(name)
        self.publish(
            TOPIC_STATE,
            json.dumps(
                {"state": "joined", "data": {"players": self.session.players_data()}}
            ),
        )
        # print("player joined: ", name)
        # if len(self.session.players) == 2:
        #     print(self.session.players)
        #     print("session is full and game can begin: ", name)
        #
        #     self.publish(
        #         TOPIC_STATE,
        #         json.dumps(
        #             {
        #                 "state": "started",
        #                 "data": {
        #                     "board_state": self.session.game.board_data(),
        #                     "players": self.session.players_data(),
        #                 },
        #             }
        #         ),
        #     )

    def handle_turn(self, player, cell):
        try:
            board_state, player = self.session.take_turn(player, cell)
            print(board_state, player)
            if board_state == "winner":
                self.publish(
                    TOPIC_STATE,
                    json.dumps(
                        {
                            "state": "game_won",
                            "data": {
                                "board_state": self.session.game.board_data(),
                                "player": player,
                            },
                        }
                    ),
                )
            else:
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
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {
                        "state": "no_turn",
                        "data": {
                            "board_state": self.session.game.board_data(),
                            "player": player,
                        },
                    }
                ),
            )
        except WrongTurn as e:
            print(e)
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {
                        "state": "no_turn",
                        "data": {
                            "board_state": self.session.game.board_data(),
                            "player": player,
                        },
                    }
                ),
            )
        except GameOver as e:
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {
                        "state": "game_over",
                        "data": {
                            "board_state": self.session.game.board_data(),
                            "player": player,
                        },
                    }
                ),
            )
        except Exception as e:
            print(e)
            self.publish(
                TOPIC_STATE,
                json.dumps(
                    {
                        "state": "unknown",
                        "player": player,
                        "data": {
                            "board_state": self.session.game.board_data(),
                        },
                    }
                ),
            )


backend = BackendClient(mqtt.CallbackAPIVersion.VERSION2, client_id="backend_client")
backend.loop_forever()
