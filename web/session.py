from dataclasses import dataclass, field
from core.game import Game

@dataclass
class Player:
    name: str
    games_won: int = field(default=0)



@dataclass
class Session:
    player_x: Player|None = field(default=None)
    player_y: Player|None = field(default=None)
    game: Game|None = field(default=None)

    games_played: int = field(default=0)

    def start(self):
        self.game = Game()
        # prompt the x player to take a turn

if __name__ == "__main__":
    pass

