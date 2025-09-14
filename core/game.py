from dataclasses import dataclass, field

@dataclass(frozen=True)
class Game:
    board: list[int] = field(default_factory= lambda: [0,0,0,0,0,0,0,0,0])

    def game_loop():
        pass


    def board_state(state):
        return self.board

    def set_cell(self, index, value):
        try:
          self.board[index] = value


    def take_turn(self, index, value):
        self.set_cell
    def possible_wins(self):
        """
          all rows and columns and diagonals, to be used to calculate the winner
        """
        ra = self.board[:2]
        rb = self.board[3:5]
        rc = self.board[6:]
        ca = [self.board[i] for i in (0,3,6)]
        cb = list(map(lambda i: i+1, ca))
        cc = list(map(lambda i: i+1, cb))
        diag = [self.board[i] for i in (0,4,-1)]
        diagb = [self.board[i] for i in (2,4,6)]

        return [ra,rb,rc,ca,cb,cc,diag,diagb]

    def check_winner(self):
        target_vals = (-3,3)
        winner = next((sum(l) for l in self.possible_wins()  if sum(l) in target_vals ), 0)
        return winner
        
    def all_turns_taken(self): 
        """ if there are no 0's on the board that means the game is over
        if there is not winner and this is true, the game is a draw
        """
        return all((self.board))

    def is_draw(self):
        pass

