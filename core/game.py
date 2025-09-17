from dataclasses import dataclass, field


class Occupied(Exception):
    """the spot on the board is already taken"""

    pass


class WrongBoard(Exception):
    """wront board size on init"""

    pass


class WrongTurn(Exception):
    """same player cant go twice in a row"""

    pass


class WrongFirst(Exception):
    """x player must go first"""

    pass


class GameOver(Exception):
    """game is over"""

    pass


@dataclass
class Game:
    last_inserted: int = 0
    board: list[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0, 0, 0, 0])

    def __post_init__(self):
        if len(self.board) != 9:
            raise WrongBoard(
                f"you initialized the wrong size board, len {len(self.board)}"
            )

    def game_loop():
        pass

    def board_data(self):
        return self.board

    def board_state(self):
        board_rep = list(".........")
        print(board_rep)
        for ind, el in enumerate(board_rep):
            match self.board[ind]:
                case -1:
                    board_rep[ind] = "o"
                case 1:
                    board_rep[ind] = "x"
                case 0:
                    board_rep[ind] = "."

        newb = []
        ind = 0
        while board_rep:
            char = board_rep.pop(0)
            if ind % 3 == 0:
                newb.append("\n")
            newb.append(char)
            ind += 1
        return "".join(newb)

        return self.board

    def take_turn(self, index, value):
        if self.all_turns_taken():
            return "start"
        if self.check_winner() == "x" or self.check_winner() == "o":
            raise GameOver(f"Game is over and {self.check_winner()} is winner")

        if self.last_inserted == 0 and value == -1:
            raise WrongFirst("x player must start")
        if value == self.last_inserted:
            raise WrongTurn("no turns twice in a row")
        if self.board[index]:  # if it is not zero it is already taken
            raise Occupied("already taken")
        else:
            self.board[index] = value
            self.last_inserted = value  # helps determine who goes next

    def possible_wins(self):
        """
        all rows and columns and diagonals, to be used to calculate the winner
        """
        ra = [self.board[i] for i in range(0, 3)]
        rb = [self.board[i] for i in range(3, 6)]
        rc = [self.board[i] for i in range(6, 9)]
        ca = [self.board[i] for i in (0, 3, 6)]
        cb = [self.board[i] for i in (1, 4, 7)]
        cc = [self.board[i] for i in (2, 5, 8)]
        diag = [self.board[i] for i in (0, 4, -1)]
        diagb = [self.board[i] for i in (2, 4, 6)]

        return [ra, rb, rc, ca, cb, cc, diag, diagb]

    def check_winner(self):
        target_vals = (-3, 3)
        for pw in self.possible_wins():
            match sum(pw):
                case 3:
                    return "x"
                case -3:
                    return "o"

        if self.all_turns_taken():
            return "draw"
        else:
            return "take another turn"

    def all_turns_taken(self):
        """if there are no 0's on the board that means the game is over
        if there is not winner and this is true, the game is a draw
        """
        return all((self.board))

    def is_draw(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.take_turn(4, -1)
    print(game.check_winner())
    print(game.board)
    print(game.check_winner())
