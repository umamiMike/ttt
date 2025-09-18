from dataclasses import dataclass, field
from core.game import Game, GameOver


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

        if len(self.players) > 1:
            return "none", 0

        if not self.players:
            player_ob = Player(name=player, order=1)
            self.players.append(player_ob)
        else:
            player_ob = Player(name=player, order=-1)
            self.players.append(player_ob)

        return player_ob.name, player_ob.order

    def take_turn(self, player: str, cell):
        player = next((plyr for plyr in self.players if plyr.name == player), None)
        if player:
            try:
                self.game.take_turn(cell, player.order)
            except GameOver as e:
                player.games_won += 1
                print(player)
        return self.game.board_data(), player.name


if __name__ == "__main__":
    pass
