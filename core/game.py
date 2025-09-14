from dataclasses import dataclass, field

class Occupied(Exception):
    """the spot on the board is already taken"""
    pass


@dataclass(frozen=True)
class Game:
    board: list[int] = field(default_factory= lambda: [0,0,0,0,0,0,0,0,0])

    def game_loop():
        pass


    def board_state(state):
        return self.board

    def take_turn(self, index, value):
        if(self.board[index]): # if it is not zero it is already taken
            raise Occupied("already taken");
        else:
          self.board[index] = value

    def possible_wins(self):
        """
          all rows and columns and diagonals, to be used to calculate the winner
        """
        ra = [self.board[i] for i in range(0,3)]
        rb = [self.board[i] for i in range(3,6)]
        rc = [self.board[i] for i in range(6,9)]
        ca = [self.board[i] for i in (0,3,6)]
        cb = [self.board[i] for i in (1,4,7)]
        cc = [self.board[i] for i in (2,5,8)]
        diag = [self.board[i] for i in (0,4,-1)]
        diagb = [self.board[i] for i in (2,4,6)]

        return [ra,rb,rc,ca,cb,cc,diag,diagb]

    def check_winner(self):

        target_vals = (-3,3)
        for pw in self.possible_wins():
            print(pw)
            pass
            breakpoint()
        # winner = next((sum(l)   if sum(l) in target_vals ), 0)
        winner = 0
        return winner
        
    def all_turns_taken(self): 
        """ if there are no 0's on the board that means the game is over
        if there is not winner and this is true, the game is a draw
        """
        return all((self.board))

    def is_draw(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.take_turn(4,-1)
    print(game.check_winner())
    print(game.board)
    print(game.check_winner())
