# test_my_functions.py
import unittest
from game  import Game, Occupied, WrongBoard, WrongTurn, WrongFirst, GameOver

class TestGame (unittest.TestCase):
    def test_game_states(self):
        """ tests states of gameboard for cases"""
        # init game with empty gameboard
        game = Game()
        print(game.check_winner())
        with self.assertRaises(WrongBoard):
            game = Game(board=[1,1,1,1,1,1,1])
            print(game.check_winner())
        
        game = Game(board=[1,1,1,1,1,1,1,1,1])
        self.assertEqual(game.check_winner(), "x", "x should win")

        game = Game(board=[-1,-1,-1,1,1,0,-1,1,1])
        self.assertEqual(game.check_winner(), "o", "o should win")

        game = Game(board=[-1,0,-1,-1,1,1,1,-1,1])
        self.assertEqual(game.check_winner(), "take another turn", "the game is not over")

        game = Game(board=[-1,1,-1,-1,1,1,1,-1,1])
        self.assertEqual(game.check_winner(), "draw", "should be a draw")

        game = Game(board=[-1,0,1,-1,1,0,-1,1,0])
        self.assertEqual(game.check_winner(), "o", "o by first column")

    def test_turns_taken(self):
        """ tests states of gameboard for cases"""
        game = Game()
        with self.assertRaises(WrongFirst):
            game.take_turn(2,-1)
            # x player must start the game
        game.take_turn(1,1)
        # self.assertEqual(game.board_state(), [0,0,1,0,0,0,0,0,0], "x in index 2")
        game.take_turn(4,-1)
        # self.assertEqual(game.board_state(), [0,0,1,0,-1,0,0,0,0], "o in center")
        with self.assertRaises(WrongTurn):
            game.take_turn(6,-1)
        with self.assertRaises(Occupied):
            game.take_turn(4,1) # square already set
        game.take_turn(3,1)
        game.take_turn(6,-1)
        game.take_turn(7,1)
        game.take_turn(2,-1)
        with self.assertRaises(GameOver):
            game.take_turn(0,1)
            print(game.board_state())
            print(f"{game.check_winner()} is the winner")

if __name__ == "__main__":
    unittest.main()
