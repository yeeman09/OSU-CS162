import unittest
from CheckersGame import InvalidSquare, InvalidPlayer, OutofTurn, Checkers, Player


class MyTestCase(unittest.TestCase):
    def test_1(self):
        # test whether the players are successfully created
        game1 = Checkers()

        P1 = game1.create_player("Adam", "White")
        P2 = game1.create_player("Lucy", "Black")

        self.assertEqual(P1.get_name(), "Adam")
        self.assertEqual(P1.get_color(), "White")
        self.assertEqual(P1.get_captured_pieces_count(), 0)

        self.assertEqual(P2.get_color(), "Black")
        self.assertEqual(P2.get_king_count(), 0)

        self.assertDictEqual(game1._player, {"Adam": P1, "Lucy": P2})

    def test_2(self):
        # test the turn record method and if normal checkers can capture pieces
        game2 = Checkers()
        P1 = game2.create_player("Adam", "White")
        P2 = game2.create_player("Lucy", "Black")
        game2.play_game("Lucy", (5, 4), (4, 3))
        self.assertEqual(P2.get_captured_pieces_count(), 0)
        self.assertEqual(game2._turn, [["Lucy", (5, 4), (4, 3)]])

        game2.play_game("Adam", (2, 1), (3, 2))
        self.assertEqual(game2._turn, [["Lucy", (5, 4), (4, 3)], ["Adam", (2, 1), (3, 2)]])
        self.assertEqual(P1.get_captured_pieces_count(), 0)

        game2.play_game("Lucy", (4, 3), (2, 1))
        self.assertEqual(P2.get_captured_pieces_count(), 1)

        game2.play_game("Adam", (1, 0), (3, 2))
        self.assertEqual(P1.get_captured_pieces_count(), 1)

    def test_3(self):
        # to check if the program can successfully make a checker piece a king
        game3 = Checkers()
        P1 = game3.create_player("James", "White")
        P2 = game3.create_player("Kawaii", "Black")
        game3.play_game("Kawaii", (5, 2), (4, 3))
        game3.play_game("James", (2, 1), (3, 2))
        game3.play_game("Kawaii", (4, 3), (2, 1))
        game3.play_game("James", (2, 3), (3, 4))
        game3.play_game("Kawaii", (5, 4), (4, 5))
        game3.play_game("James", (2, 7), (3, 6))
        game3.play_game("Kawaii", (4, 5), (2, 7))
        game3.play_game("James", (3, 4), (4, 5))
        game3.play_game("Kawaii", (5, 6), (3, 4))
        game3.play_game("James", (1, 2), (2, 3))
        game3.play_game("Kawaii", (3, 4), (1, 2))
        game3.play_game("James", (0, 1), (2, 3))
        game3.play_game("Kawaii", (2, 1), (1, 2))
        game3.play_game("James", (2, 3), (3, 4))
        game3.play_game("Kawaii", (1, 2), (0, 1))   # Kawaii reaches the other end!

        self.assertEqual(P2.get_king_count(), 1)

    def test_4(self):
        # to check if king checkers can successfully capture an opponent
        game4 = Checkers()
        P1 = game4.create_player("James", "White")
        P2 = game4.create_player("Kawaii", "Black")
        game4.play_game("Kawaii", (5, 2), (4, 3))
        game4.play_game("James", (2, 1), (3, 2))
        game4.play_game("Kawaii", (4, 3), (2, 1))  # Kawaii + 1
        self.assertEqual(P2.get_captured_pieces_count(), 1)

        game4.play_game("James", (2, 3), (3, 4))
        game4.play_game("Kawaii", (5, 4), (4, 5))
        game4.play_game("James", (2, 7), (3, 6))
        game4.play_game("Kawaii", (4, 5), (2, 7))  # Kawaii + 1
        self.assertEqual(P2.get_captured_pieces_count(), 2)

        game4.play_game("James", (3, 4), (4, 5))
        game4.play_game("Kawaii", (5, 6), (3, 4))  # Kawaii + 1
        self.assertEqual(P2.get_captured_pieces_count(), 3)

        game4.play_game("James", (1, 2), (2, 3))
        game4.play_game("Kawaii", (3, 4), (1, 2))  # Kawaii + 1
        self.assertEqual(P2.get_captured_pieces_count(), 4)

        game4.play_game("James", (0, 1), (2, 3))  # James + 1
        game4.play_game("Kawaii", (2, 1), (1, 2))
        game4.play_game("James", (2, 3), (3, 4))
        game4.play_game("Kawaii", (1, 2), (0, 1)) # Kawaii King + 1
        self.assertEqual(P2.get_king_count(), 1)
        game4.play_game("James", (0, 3), (1, 2))
        game4.play_game("Kawaii", (0, 1), (2, 3))  # Kawaii King successfully captures the opponent!
        self.assertEqual(P2.get_captured_pieces_count(), 5)

        game4.play_game("Kawaii", (2, 3), (4, 5))  # Kawaii + 1
        self.assertEqual(P2.get_captured_pieces_count(), 6)

        game4.play_game("James", (1, 0), (2, 1))
        game4.play_game("Kawaii", (6, 3), (5, 2))
        game4.play_game("James", (1, 4), (2, 3))
        game4.play_game("Kawaii", (4, 5), (2, 3))   # Kawaii + 1
        self.assertEqual(P2.get_captured_pieces_count(), 7)
        self.assertEqual(P1.get_captured_pieces_count(), 1)

    def test_5(self):
        # to test if triple king can capture the opponent and whether the game winner method works
        game5 = Checkers()
        P1 = game5.create_player("Kim", "Black")
        P2 = game5.create_player("Lee", "White")

        game5.play_game("Kim", (5, 2), (4, 3))
        game5.play_game("Lee", (2, 5), (3, 4))
        game5.play_game("Kim", (4, 3), (2, 5))
        game5.play_game("Lee", (2, 3), (3, 2))
        game5.play_game("Kim", (5, 4), (4, 5))
        game5.play_game("Lee", (2, 1), (3, 0))
        game5.play_game("Kim", (6, 5), (5, 4))

        game5.play_game("Lee", (1, 4), (3, 6))
        self.assertEqual(P2.get_captured_pieces_count(), 1)
        self.assertEqual(P1.get_captured_pieces_count(), 1)

        game5.play_game("Kim", (5, 6), (4, 7))
        game5.play_game("Lee", (0, 5), (1, 4))
        game5.play_game("Kim", (6, 3), (5, 2))
        game5.play_game("Lee", (1, 4), (2, 3))
        game5.play_game("Kim", (7, 6), (6, 5))
        game5.play_game("Lee", (1, 0), (2, 1))
        game5.play_game("Kim", (7, 4), (6, 3))
        game5.play_game("Lee", (0, 3), (1, 4))
        game5.play_game("Kim", (5, 2), (4, 1))
        game5.play_game("Lee", (3, 2), (4, 3))
        game5.play_game("Kim", (5, 4), (3, 2))
        game5.play_game("Kim", (3, 2), (1, 0))
        game5.play_game("Lee", (3, 0), (5, 2))
        game5.play_game("Lee", (5, 2), (7, 4))

        self.assertEqual(P1.get_captured_pieces_count(), 3)
        self.assertEqual(P2.get_captured_pieces_count(), 3)

        game5.play_game("Kim", (4, 7), (2, 5))
        game5.play_game("Kim", (2, 5), (0, 3))
        self.assertEqual(P1.get_captured_pieces_count(), 5)

        game5.play_game("Lee", (7, 4), (5, 6))
        game5.play_game("Lee", (5, 6), (3, 4))
        self.assertEqual(P2.get_captured_pieces_count(), 5)
        self.assertEqual(P1.get_king_count(), 1)
        self.assertEqual(P2.get_king_count(), 1)

        game5.play_game("Kim", (5, 0), (4, 1))
        game5.play_game("Lee", (3, 4), (2, 5))
        game5.play_game("Kim", (0, 3), (4, 7))
        self.assertEqual(P1.get_captured_pieces_count(), 6)

        game5.play_game("Lee", (2, 3), (3, 2))
        game5.play_game("Kim", (4, 1), (2, 3))
        self.assertEqual(P1.get_captured_pieces_count(), 7)

        game5.play_game("Lee", (1, 6), (2, 5))
        game5.play_game("Kim", (4, 7), (5, 6))
        game5.play_game("Lee", (1, 2), (3, 4))
        self.assertEqual(P2.get_captured_pieces_count(), 6)

        game5.play_game("Kim", (5, 6), (6, 5))
        game5.play_game("Lee", (3, 4), (4, 3))
        game5.play_game("Kim", (6, 5), (7, 4))
        game5.play_game("Lee", (4, 3), (5, 4))
        game5.play_game("Kim", (6, 1), (5, 2))
        game5.play_game("Lee", (2, 5), (3, 4))
        game5.play_game("Kim", (7, 4), (3, 0))
        game5.play_game("Lee", (0, 1), (1, 2))
        game5.play_game("Kim", (3, 0), (0, 3))
        self.assertEqual(P1.get_captured_pieces_count(), 8)     # Triple King works!

        game5.play_game("Lee", (0, 7), (1, 6))
        game5.play_game("Kim", (7, 2), (6, 3))
        game5.play_game("Lee", (1, 6), (2, 5))
        game5.play_game("Kim", (6, 3), (4, 5))
        self.assertEqual(P1.get_captured_pieces_count(), 9)

        game5.play_game("Lee", (2, 7), (3, 6))
        game5.play_game("Kim", (0, 3), (4, 7))
        self.assertEqual(P1.get_captured_pieces_count(), 11)    # Black Triple King successfully eats 2!

        game5.play_game("Lee", (3, 4), (5, 6))
        game5.play_game("Kim", (4, 7), (6, 5))
        self.assertEqual(P1.get_captured_pieces_count(), 12)
        self.assertIs(game5.game_winner(), "Kim")               # game winner works!


if __name__ == '__main__':
    unittest.main()
