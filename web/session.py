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

        return self.players

    def players_data(self):
        pd = [{"player": p.name, "order": p.order} for p in self.players]
        return pd

    def take_turn(self, player: str, cell):
        # print("incoming player name to check")
        # print(player)
        # print(self.players_data())
        player = next((plyr for plyr in self.players if plyr.name == player), None)
        if player:
            try:
                self.game.take_turn(cell, player.order)
                if self.game.check_winner() != "take another turn":
                    return "winner", player.name
            except GameOver as e:
                player.games_won += 1
            return self.game.board_data(), player.name


if __name__ == "__main__":
    pass
