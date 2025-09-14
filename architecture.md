## game
This is core functionality
Tracks the evolving state of a single game

minimax algorithm

possible states
x wins
o wins
draw

each cell in the 3x3 grid has an index

these are the indices for the array
if 012 sum to 3 or -3
if 345 sum to 3 or -3
if 678 sum to 3 or -3
if 0 4 8 sum to 3 or -3
if 2 4 6 sum to 3 or -3

if 3 x wins
if -3 o wins

if there are no 0's left but the other checks dont match

```python

@dataclass(frozen=True)
class Round:
    winner=None
    player_up: str= "x"

class Game
# core logic for winning game
@dataclass(frozen=True)
class TicTacToe:
    board: list[int] = filed(default=[0,0,0,0,0,0,0,0,0], 



def possible_wins(self)
    """
      all rows and columns and diagonals, to be used to calculate the winner
    """
    ra = self.board[:2]
    rb = self.board[3:5]
    rc = self.board[6:]
    ca = [self.board[i] for i in (0,3,6)]
    cb = list(map(lambda i: i+1, ca)
    cc = list(map(lambda i: i+1, cb)
    diag = [self.board[i] for i in (0,4,-1)]
    diagb = [self.board[i] for i in (2,4,6)]
    return [ra,rb,rc,ca,cb,cc,diag,diagb]

    def winner_is(self):
        target_vals = (-3,3)
        # search through a list of slices and return that target value, otherwise return 0
        winner = next((sum(l) for l in self.possible_wins()  if sum(l) in target_vals ), 0):
        return winner
        
    def check_board(self)
        # possible success


    def all_turns_taken = (self)
        """ if there are no 0's on the board that means the game is over
        if there is not winner and this is true, the game is a draw
        """
        return all((self.board))

    def is_draw(self):


```
initialized

gameboard = [0,0,0,0,0,0,0,0,0]

···
···
···

the x player goes and picks the center

···
·x·
···

gameboard = [0,0,0,0,1,0,0,0,0]

the sum of the board is 1
---

the o player picks the lower right

···
·x·
··o

gameboard = [0,0,0,0,1,0,0,0,-1]

---

The sum of the board is now 0.

---

later on x will win
··x
·xo
x·o

but what of a draw
o·x
xxo
oxo


## player

has a name
plays a game against another player

## session
- triggered when a player attempts a valid `join_session`
Tracks all the games for a set of players
the score for each player for each game they have won
the number of draws

is started by the server

## server

- starts a web based endpoint
- allows for the command line client to connect to a session

## endpoints

### api

`/ ` 

serves index.html, the game board for a player to join a game

```
/api/
```

- `POST /connect/{player_id}`
- `GET /player/{player_id}`

### game session streaming endpoint

`wss://api/sessions/{session_id}/stream`


**client -> server**
to join a session

```json
{
"action": "join_session",
"player_id": "playername",
}
```


**server -> client**
```json
{
"event": "player_joined",
"data": {"status": waiting},
}
```





