# test_my_functions.py
import unittest
from game  import Game, WrongBoard

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



if __name__ == "__main__":
    unittest.main()
