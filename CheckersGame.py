# Author: Minyi Huang
# GitHub username: yeeman09
# Date: Mar 11th, 2023
# Description: Checkers Game

class InvalidPlayer(Exception):
    """
    The player name does not exist
    """
    pass


class OutofTurn(Exception):
    """
    The player attempts to move a piece out of turn
    """
    pass


class InvalidSquare(Exception):
    """
    The player does not own the checker in the square
    or the square does not exist
    """
    pass


class Player:
    """
    Represents a player with the name and the checker color
    """

    def __init__(self, player_name, checker_color):
        self._name = player_name
        self._color = checker_color
        self._king = 0
        self._triple_king = 0
        self._captured_pieces = 0

    def get_name(self):
        """
        Returns the name of the player
        """
        return self._name

    def get_color(self):
        """
        Returns the checker color of the player
        """
        return self._color

    def add_king(self, count):
        """
        Adds the number of king
        """
        self._king += count
        return

    def get_king_count(self):
        """
        Returns the number of king pieces that the player has
        """
        return self._king

    def add_triple_king(self, count=1):
        """
        Adds the number of triple king
        """
        self._triple_king += count
        return

    def get_triple_king_count(self):
        """
        Returns the number of the triple king pieces that the player has
        """
        return self._triple_king

    def add_captured_pieces_count(self, count):
        """
        Adds the number of captured piece in one move
        """
        self._captured_pieces += count
        return

    def get_captured_pieces_count(self):
        """
        Returns the number of opponent pieces that the player has captured
        """
        return self._captured_pieces


class Checkers:

    def __init__(self):
        self._player = {}           # {"name": player object}
        self._turn = []      # ["name", (x1, y1), (x2, y2)]
        self._capture_record = []
        self._board = [[None, "White", None, "White", None, "White", None, "White"],
                       ["White", None, "White", None, "White", None, "White", None],
                       [None, "White", None, "White", None, "White", None, "White"],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       ["Black", None, "Black", None, "Black", None, "Black", None],
                       [None, "Black", None, "Black", None, "Black", None, "Black"],
                       ["Black", None, "Black", None, "Black", None, "Black", None]]

    def create_player(self, player_name, piece_color):
        """
        Returns a player object
        """
        player = Player(player_name, piece_color)
        self._player[player_name] = player
        return player

    def turn_record(self, player_name, start, stop):
        """
        Records each turn (each call of the play_game method)
        """
        self._turn += [[player_name, start, stop]]
        return

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        Returns how many opponents the player has captured in this turn
        """
        checker = self.get_checker_details(starting_square_location)

        # 1. Check for player name Exception
        if player_name not in self._player:
            raise InvalidPlayer

        # 2. Check for Out of Turn Exception
        if len(self._turn) > 1 and player_name == self._turn[-1][0]:
            # if the starting square was not the previous destination, then this move will not be validated
            if starting_square_location != self._turn[-1][2]:
                raise OutofTurn

            # for normal and king checker, if the previous move was not a capturing move,
            # then this move will not be validated
            elif abs(self._turn[-1][2][1] - self._turn[-1][1][1]) < 2:
                raise OutofTurn

            # for triple king checker, if the previous move column >= 2,
            # check whether TK checker simply hops over the friendly piece or is indeed capturing
            elif checker == "White_Triple_King" and abs(self._turn[-1][2][1] - self._turn[-1][1][1]) >= 2:
                if self._capture_record[-1] != player_name:
                    raise OutofTurn

            elif checker == "Black_Triple_King" and abs(self._turn[-1][2][1] - self._turn[-1][1][1]) >= 2:
                if self._capture_record[-1] != player_name:
                    raise OutofTurn

            # if the current move is not a capturing move, then this move will not be validated
            elif abs(destination_square_location[1] - starting_square_location[1]) < 2:
                raise OutofTurn

        # 3. Check for Invalid Square Exception, make sure the row and column range is [0, 7]
        if starting_square_location[0] > 7 or starting_square_location[1] > 7:
            raise InvalidSquare

        if starting_square_location[0] < 0 or starting_square_location[1] < 0:
            raise InvalidSquare

        if destination_square_location[0] > 7 or destination_square_location[1] > 7:
            raise InvalidSquare

        if destination_square_location[0] < 0 or destination_square_location[1] < 0:
            raise InvalidSquare

        # 4. Check for the starting square location, if validated, then turn it into None
        for row in range(0, 8):
            if row == starting_square_location[0]:
                for col in range(0, 8):
                    if col == starting_square_location[1]:
                        if self._board[row][col] is None:
                            raise InvalidSquare

                        elif self._board[row][col] != checker:
                            raise InvalidSquare

                        else:
                            self._board[row][col] = None

        # 5. Make the move, change the destination into the piece color/ king/ triple king
        for row in range(0, 8):
            if row == destination_square_location[0]:
                for col in range(0, 8):
                    if col == destination_square_location[1]:
                        self._board[row][col] = checker

                        # 5. 1 Make the piece a king
                        if checker == "White" and destination_square_location[0] == 7:
                            self._player[player_name].add_king(1)
                            self._board[row][col] = "White_king"

                        if checker == "Black" and destination_square_location[0] == 0:
                            self._player[player_name].add_king(1)
                            self._board[row][col] = "Black_king"

                        # 5. 2 Make the king the Triple King
                        if checker == "White_king" and destination_square_location[0] == 0:
                            self._player[player_name].add_triple_king(1)
                            self._board[row][col] = "White_Triple_King"

                        if checker == "Black_king" and destination_square_location[0] == 7:
                            self._player[player_name].add_triple_king(1)
                            self._board[row][col] = "Black_Triple_King"

        # 6. Since the move is validated, record it to be used in checking Out of Turn Exception
        self.turn_record(player_name, starting_square_location, destination_square_location)

        # 7. Calculate the captured piece, record the player who makes a captured move,
        #    and make the captured piece None
        captured_piece = 0

        if checker == "Black" or checker == "White":
            result = self.normal_checker_play(starting_square_location, destination_square_location, captured_piece)

        if checker == "Black_king" or checker == "White_king":
            result = self.king_checker_play(starting_square_location, destination_square_location, checker,
                                            captured_piece)

        if checker == "Black_Triple_King" or checker == "White_Triple_King":
            result = self.triple_king_checker_play(starting_square_location, destination_square_location, checker,
                                                   captured_piece)

        captured_piece += result
        self._player[player_name].add_captured_pieces_count(captured_piece)

        if captured_piece > 0:
            self._capture_record.append(player_name)
        else:
            self._capture_record.append(None)

        return captured_piece

    def get_checker_details(self, square_location):
        """
        Returns the checker details corresponding to the square location
        """

        # 1. Check for Invalid Square Exception
        if square_location[0] > 7 or square_location[1] > 7:
            raise InvalidSquare

        # 2. Return Checker details
        for row in range(0, 8):
            if row == square_location[0]:
                for col in range(0, 8):
                    if col == square_location[1]:
                        # if no piece is present in the location
                        if self._board[row][col] is None:
                            return None

                        elif self._board[row][col] == "Black":
                            return "Black"

                        elif self._board[row][col] == "White":
                            return "White"

                        elif self._board[row][col] == "Black_king":
                            return "Black_king"

                        elif self._board[row][col] == "White_king":
                            return "White_king"

                        elif self._board[row][col] == "Black_Triple_King":
                            return "Black_Triple_King"

                        elif self._board[row][col] == "White_Triple_King":
                            return "White_Triple_King"

    def print_board(self):
        """
        Print the CURRENT board
        """
        for row in self._board:
            print(row)

    def game_winner(self):
        """
        Return the game winner if any, else return 'Game has not ended'
        """
        for player in self._player:
            if self._player[player].get_captured_pieces_count() == 12:
                return player

        return "Game has not ended"

    def normal_checker_play(self, starting_square_location, destination_square_location, captured_piece):
        """
        If the checker is a normal checker, then returns its number of captured piece according to the rules
        """
        start_x = starting_square_location[0]
        start_y = starting_square_location[1]

        des_x = destination_square_location[0]
        des_y = destination_square_location[1]

        crossed_col = des_y - start_y
        crossed_row = des_x - start_x

        if abs(crossed_col) == 2:
            self.two_columns_move(start_x, start_y, crossed_col, crossed_row)
            captured_piece += 1

        return captured_piece

    def king_checker_play(self, starting_square_location, destination_square_location, checker, captured_piece):
        """
        If the checker is a king checker, then returns its number of captured piece according to the rules
        """
        start_x = starting_square_location[0]
        start_y = starting_square_location[1]

        des_x = destination_square_location[0]
        des_y = destination_square_location[1]

        crossed_col = des_y - start_y
        crossed_row = des_x - start_x

        if abs(crossed_col) < 2:
            return captured_piece

        if abs(crossed_col) == 2:
            self.two_columns_move(start_x, start_y, crossed_col, crossed_row)
            captured_piece += 1
            return captured_piece

        if abs(crossed_col) > 2:
            return self.multiple_columns_move(start_x, start_y, des_y, crossed_col, crossed_row, checker,
                                              captured_piece)

    def triple_king_checker_play(self, starting_square_location, destination_square_location, checker, captured_piece):
        """
        If the checker is a triple king checker, then returns its number of captured piece according to the rules
        """
        start_x = starting_square_location[0]
        start_y = starting_square_location[1]

        des_x = destination_square_location[0]
        des_y = destination_square_location[1]

        crossed_col = des_y - start_y
        crossed_row = des_x - start_x

        if abs(crossed_col) < 2:
            return captured_piece

        if abs(crossed_col) >= 2:
            return self.multiple_columns_move(start_x, start_y, des_y, crossed_col, crossed_row, checker,
                                              captured_piece)

    def two_columns_move(self, start_x, start_y, crossed_col, crossed_row):
        """
        If the checker (specified to normal and king checker) moves two columns,
        then it must have captured an opponent piece, make the captured piece None
        """
        if crossed_col < 0:  # move leftward
            start_y -= 1
            if crossed_row < 0:  # move left & upward
                start_x -= 1
                self._board[start_x][start_y] = None

            else:  # move left & downward
                start_x += 1
                self._board[start_x][start_y] = None

        else:
            start_y += 1  # move rightward
            if crossed_row < 0:  # move right & upward
                start_x -= 1
                self._board[start_x][start_y] = None

            else:  # move right & downward
                start_x += 1
                self._board[start_x][start_y] = None

    def multiple_columns_move(self, start_x, start_y, des_y, crossed_col, crossed_row, checker, captured_piece):
        """
        If the checker (specified to king and triple king) moves multiple columns,
        checks for how many opponent it has captured
        """
        if crossed_col < 0:  # move leftward
            while des_y < start_y:
                start_y = start_y - 1
                if crossed_row < 0:  # move up and leftward
                    start_x -= 1
                    result = self.king_capturing(start_x, start_y, checker)

                else:  # move down and leftward
                    start_x += 1
                    result = self.king_capturing(start_x, start_y, checker)

                captured_piece += result

        else:  # move rightward
            while start_y < des_y:
                start_y = start_y + 1
                if crossed_row < 0:  # move up and rightward
                    start_x -= 1
                    result = self.king_capturing(start_x, start_y, checker)

                else:  # move down and rightward
                    start_x += 1
                    result = self.king_capturing(start_x, start_y, checker)

                captured_piece += result

        return captured_piece

    def king_capturing(self, start_x, start_y, checker):
        """
        If the checker is a king or triple king checker, then this method will check how many
        opponents it has captured along its moving path
        """
        captured_piece = 0

        # 1. Check whether it is a white/ black king
        if checker == "Black_king" or checker == "Black_Triple_King":

            # 2. Check checkers on the moving path
            checker_on_the_path = self.get_checker_details((start_x, start_y))
            if checker_on_the_path == "White":
                captured_piece += 1
                self._board[start_x][start_y] = None

            elif checker_on_the_path == "White_king":
                captured_piece += 1
                self._board[start_x][start_y] = None

            elif checker_on_the_path == "White_Triple_King":
                captured_piece += 1
                self._board[start_x][start_y] = None

            else:
                captured_piece += 0

        if checker == "White_king" or checker == "White_Triple_King":
            checker_on_the_path = self.get_checker_details((start_x, start_y))
            if checker_on_the_path == "Black":
                captured_piece += 1
                self._board[start_x][start_y] = None

            elif checker_on_the_path == "Black_king":
                captured_piece += 1
                self._board[start_x][start_y] = None

            elif checker_on_the_path == "Black_Triple_King":
                captured_piece += 1
                self._board[start_x][start_y] = None

            else:
                captured_piece += 0

        return captured_piece
