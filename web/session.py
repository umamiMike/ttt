from dataclasses import dataclass, field
from core.game import Game


@dataclass
class Player:
    name: str
    order: int
    games_won: int = field(default=0)


@dataclass
class Session:
    players: list[Player] = field(default_factory=list)
    game: Game | None = field(default=None)
    games_played: int = field(default=0)

    def __post_init__(self):
        self.game = Game()

    def join(self, player):
        if not self.players:
            self.players.append(Player(name=player, order=1))

            print("players: ", self.players)
        return True

    def take_turn(self, player, cell):
        player = next((plyr for plyr in self.players if plyr.name == player), None)
        print(player)
        if player:
            self.game.take_turn(cell, player.order)


if __name__ == "__main__":
    pass
