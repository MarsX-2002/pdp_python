import unittest
from game1.game import add_orb, check_explosions, evaluate_board

class TestGameFunctions(unittest.TestCase):

    def test_add_orb(self):
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertTrue(add_orb(board, 0, 0, 1, 1))
        self.assertEqual(board[0][0], 1)
        self.assertFalse(add_orb(board, 0, 0, -1, -1))
        self.assertEqual(board[0][0], 1)

    def test_check_explosions(self):
        board = [[0, 0, 0], [0, 3, 0], [0, 0, 0]]
        check_explosions(board, 1, 1, 1)
        self.assertEqual(board[1][1], 0)
        self.assertEqual(board[0][1], 1)
        self.assertEqual(board[2][1], 1)

    def test_evaluate_board(self):
        board = [[1, -1, 1], [-1, 1, -1], [1, -1, 1]]
        score = evaluate_board(board)
        self.assertEqual(score, 0)