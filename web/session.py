from dataclasses import dataclass, field
from core.game import Game

@dataclass
class Player:
    name: str
    games_won: int = field(default=0)



@dataclass
class Session:
    player_x: Player
    player_y: Player

    games_played: int = field(default=0)

    def start(self):
        game = Game()
        # prompt the x player to take a turn
        print(game.check_winner())

    # a player connects, now we are waiting for another  player to connect to
    # connects the players and a set of games they play

if __name__ == "__main__":
    pass

