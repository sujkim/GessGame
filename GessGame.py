# Date: 3 Jun 2020
# Description: A Gess game simulator that has a Move class, Board class, and Gess Game class. The Move
#               class represents a move from one center square to another and has methods to check the
#               distance of a move, the direction of a move, and a list of squares the move passes
#               along the way. The Board class represents a Gess board


class Move:
    """represents a move of a piece on a Gess Board from one center square to another center square"""

    def __init__(self, from_location, to_location):
        """creates a Move object with a from location to a to location represented by a center square"""
        self._from_row = int(from_location[1:]) - 1
        self._from_column = ord(from_location[0]) - 97
        self._to_row = int(to_location[1:]) - 1
        self._to_column = ord(to_location[0]) - 97
        self._from_square = from_location
        self._to_square = to_location

    def check_distance(self):
        """returns the row distance and column distance of a move"""

        row_distance = self._to_row - self._from_row
        column_distance = self._to_column - self._from_column

        return row_distance, column_distance

    def check_direction(self):
        """returns the direction of a move with possible directions (NE, N, NW, W, C, E, SW, S, SE)"""

        row_distance = self.check_distance()[0]
        column_distance = self.check_distance()[1]

        if row_distance == column_distance:
            if row_distance > 0:
                return 'NE'
            else:
                return 'SW'

        if row_distance == -column_distance:
            if row_distance > 0:
                return 'NW'
            else:
                return 'SE'

        if column_distance == 0:
            if row_distance > 0:
                return 'N'
            else:
                return 'S'

        if row_distance == 0:
            if column_distance < 0:
                return 'W'
            else:
                return 'E'

        else:
            return False

    def traversed_squares(self):
        """returns a list of locations a move traverses"""

        direction = self.check_direction()
        row_distance = abs(self.check_distance()[0])
        column_distance = abs(self.check_distance()[1])
        column = ord(self._from_square[0])
        row = int(self._from_square[1:])

        visited_squares = []

        if direction == 'NW':
            for x in range(1, row_distance + 1):
                next_square = chr(column - x) + str(row + x)
                visited_squares.append(next_square)

        if direction == 'N':
            for x in range(1, row_distance + 1):
                next_square = chr(column) + str(row + x)
                visited_squares.append(next_square)

        if direction == 'NE':
            for x in range(1, row_distance + 1):
                next_square = chr(column + x) + str(row + x)
                visited_squares.append(next_square)

        if direction == 'W':
            for x in range(1, column_distance + 1):
                next_square = chr(column - x) + str(row)
                visited_squares.append(next_square)

        if direction == 'E':
            for x in range(1, column_distance + 1):
                next_square = chr(column + x) + str(row)
                visited_squares.append(next_square)

        if direction == 'SW':
            for x in range(1, column_distance + 1):
                next_square = chr(column - x) + str(row - x)
                visited_squares.append(next_square)

        if direction == 'S':
            for x in range(1, row_distance + 1):
                next_square = chr(column) + str(row - x)
                visited_squares.append(next_square)

        if direction == 'SE':
            for x in range(1, row_distance + 1):
                next_square = chr(column + x) + str(row - x)
                visited_squares.append(next_square)

        return visited_squares


class Board:
    """represents a Gess Board with methods to update board, clear the edge of board of stones,
    return the footprint (3x3 area) of a given center square location, erase a footprint, check
      if a location holds a player's piece, moves a piece, returns the rings on the board, and checks if
        a move is legal"""

    def __init__(self):
        """initializes an empty Board"""
        self._board = [['_'] * 20 for n in range(20)]

    def get_row_column(self, location):
        """returns board row index and column index given board location"""
        row = int(location[1:]) - 1  # convert row to index
        column = ord(location[0]) - 97  # convert column to index

        return row, column

    def get_board(self):
        """returns the board"""
        return self._board

    def update_board(self, board):
        """replaces board with given board"""
        self._board = board

    def clear_edges(self):
        """removes any stones on the board's edges by replacing with empty squares"""
        self._board[0][0:20] = '_' * 20
        self._board[19][0:20] = '_' * 20
        for row in self._board:
            row[0] = '_'
        for row in self._board:
            row[19] = '_'

    def get_footprint(self, center_square):
        """returns the contents of a 3x3 footprint as a list of rows given the center square"""
        row = self.get_row_column(center_square)[0]
        column = self.get_row_column(center_square)[1]
        left = column - 1
        right = column + 2

        try:
            footprint = [
                self._board[row + 1][left:right],
                self._board[row][left:right],
                self._board[row - 1][left:right]]
        except IndexError:
            return False

        return footprint

    def get_stones(self, center_square):
        """returns a list of stone directions in a piece"""

        # piece represented by a 3x3 footprint of board with a center square
        try:
            piece = self.get_footprint(center_square)
            # dictionary of directions with corresponding element of list
            stone_direction = {
                "NW": piece[0][0],
                "N": piece[0][1],
                "NE": piece[0][2],
                "W": piece[1][0],
                "C": piece[1][1],
                "E": piece[1][2],
                "SW": piece[2][0],
                "S": piece[2][1],
                "SE": piece[2][2]
            }
        except IndexError:
            return False

        # initialize empty list of stones
        list_stones = []

        # if a 'B' or 'W' is present in the piece, add to list of stones
        for key, value in stone_direction.items():
            if value == 'B' or value == 'W':
                list_stones.append(key)

        return list_stones

    def erase_footprint(self, center_square):
        """erases 3x3 area around given center_square, on the board"""

        row = self.get_row_column(center_square)[0]
        column = self.get_row_column(center_square)[1]
        left = column - 1
        right = column + 2

        # erase stones on the board
        self._board[row + 1][left:right] = ['_', '_', '_']
        self._board[row][left:right] = ['_', '_', '_']
        self._board[row - 1][left:right] = ['_', '_', '_']

    def valid_piece(self, center_square):
        """returns which player's piece is at a given location and returns False if
        piece is not a moveable piece"""

        # if only center stone, can't move
        if self.get_stones(center_square) == ['C']:
            return False

        # if only black or white stones in the footprint, return that player
        for squares in self.get_footprint(center_square):
            if 'B' in squares and 'W' not in squares:
                return "BLACK"
            if 'W' in squares and 'B' not in squares:
                return "WHITE"
        else:
            return False

    def move_piece(self, original_location, new_location):
        """given a piece, places that piece at a given location, and removes from
        original location"""

        piece = self.get_footprint(original_location)  # piece to be moved
        self.erase_footprint(original_location)  # erase footprint at original location

        # get row and column index of new location
        location_row = self.get_row_column(new_location)[0]
        location_column = self.get_row_column(new_location)[1]

        # move footprint to new location
        self._board[location_row - 1][location_column - 1:location_column + 2] = piece[0]
        self._board[location_row][location_column - 1:location_column + 2] = piece[1]
        self._board[location_row + 1][location_column - 1:location_column + 2] = piece[2]

    def get_location(self, row_index, column_index):
        """returns board location given board row and column index"""
        row_index = row_index + 1
        column_index = chr(column_index + 97)

        location = column_index + str(row_index)

        return location

    def get_all_locations(self):
        """returns all possible playable locations on the board """
        all_locations = []

        for row_index in range(1, 19):
            for column_index in range(1, 19):
                all_locations.append(self.get_location(row_index, column_index))

        return all_locations

    def ring_piece(self):
        """returns dictionary of rings on the board"""

        # initialize empty dictionary of rings
        rings = {}

        # for all the locations on the board, check all valid pieces, check if they are rings
        for locations in self.get_all_locations():
            if (
                    self.valid_piece(locations) == "BLACK" and
                    self.get_stones(locations) == ["NW", "N", "NE", "W", "E", "SW", "S", "SE"]):
                rings["BLACK"] = locations
            elif (
                    self.valid_piece(locations) == "WHITE" and
                    self.get_stones(locations) == ["NW", "N", "NE", "W", "E", "SW", "S", "SE"]):
                rings["WHITE"] = locations

        return rings

    def check_obstruction(self, from_square, to_square):
        """returns location that piece stops if there's an obstruction, otherwise, returns
        destination square if no obstruction along the way"""

        move = Move(from_square, to_square)

        # save copy of board
        temp_board = []
        for i in self._board:
            temp_board.append(list(i))

        # erase starting piece
        self.erase_footprint(from_square)

        # for all locations traversed in a move, check if there are stones on path
        for squares in move.traversed_squares():
            footprint = self.get_footprint(squares)
            for spaces in footprint:
                if 'B' in spaces or 'W' in spaces:  # if stone encountered in a footprint, return location
                    self._board = temp_board  # revert to original board
                    return squares

        else:
            self._board = temp_board  # revert to original board
            return to_square  # if no stones encountered, return to square

    def valid_move(self, from_square, to_square, player):
        """returns True if move is allowed else returns False"""

        move = Move(from_square, to_square)

        # if piece is out of bounds
        try:
            self.get_footprint(from_square)
        except IndexError:
            return False

        # if piece being moved is not player's piece
        if self.valid_piece(from_square) != player:
            return False

        # if direction stone not present or obstructed before destination
        if (
                move.check_direction() not in self.get_stones(from_square) or
                self.check_obstruction(from_square, to_square) != to_square):
            return False

        # if there is no center stone, and moves more than 3 squares, return False
        if 'C' not in self.get_stones(from_square):
            if move.check_direction() == 'N' or move.check_direction() == 'S':
                if abs(move.check_distance()[0]) not in range(1, 4):
                    return False
            if move.check_direction() == 'NE' or move.check_direction() == 'SE':
                if abs(move.check_distance()[0]) not in range(1, 4):
                    return False
            if move.check_direction() == 'NW' or move.check_direction() == 'SW':
                if abs(move.check_distance()[0]) not in range(1, 4):
                    return False
            if move.check_direction() == 'W' or move.check_direction() == 'E':
                if abs(move.check_distance()[1]) not in range(1, 4):
                    return False

        return True


class GessGame:
    """represents a GessGame with methods to resign a game, make a move, and keeps
    track of game state and player's turn. """

    def __init__(self):
        """initializes a board with starting positions, game state to unfinished, and
        black goes first"""
        self._board = [['_'] * 20 for n in range(20)]
        self._board[18][2], self._board[18][4] = 'W' * 2
        self._board[18][6:14] = 'W' * 8
        self._board[18][15], self._board[18][17] = 'W' * 2
        self._board[17][1:4] = 'W' * 3
        self._board[17][5], self._board[17][12], self._board[17][14] = 'W' * 3
        self._board[17][7:11] = 'W' * 4
        self._board[17][16:19] = 'W' * 3
        self._board[16][2], self._board[16][4] = 'W' * 2
        self._board[16][15], self._board[16][17] = 'W' * 2
        self._board[16][6:14] = 'W' * 8
        self._board[13][2:18:3] = 'W' * 6
        self._board[1][2], self._board[1][4] = 'B' * 2
        self._board[1][6:14] = 'B' * 8
        self._board[1][15], self._board[1][17] = 'B' * 2
        self._board[2][1:4] = 'B' * 3
        self._board[2][5], self._board[2][12], self._board[2][14] = 'B' * 3
        self._board[2][7:11] = 'B' * 4
        self._board[2][16:19] = 'B' * 3
        self._board[3][2], self._board[3][4] = 'B' * 2
        self._board[3][15], self._board[3][17] = 'B' * 2
        self._board[3][6:14] = 'B' * 8
        self._board[6][2:18:3] = 'B' * 6
        self._game_state = "UNFINISHED"
        self._player_turn = "BLACK"

    def get_board(self):
        """returns board"""
        return self._board

    def print_board(self):
        """prints board"""
        row_number = 20
        for row in reversed(self._board):
            print(row, row_number)
            row_number -= 1
        column = [chr(x) for x in range(97, 117)]
        print(column)

    def get_game_state(self):
        """returns game state"""
        return self._game_state

    def get_player_turn(self):
        """returns which player's turn it is"""
        return self._player_turn

    def resign_game(self):
        """changes the game state to whoever is not the current player the win"""

        if self._player_turn == "BLACK":
            self._game_state = "WHITE_WON"

        if self._player_turn == "WHITE":
            self._game_state = "BLACK_WON"

    def make_move(self, start_location, new_location):
        """makes a move from a given starting position to new position, updates the board,
         checks if move resulted in a win and updates player's turn -- if move is illegal,
        or game is already won, returns False"""

        move = Move(start_location, new_location)
        board = Board()

        # update board with current game board
        board.update_board(self._board)

        # check if move legal
        if board.valid_move(start_location, new_location, self._player_turn) is False:
            return False

        # if game already won
        if self._game_state == "WHITE_WON" or self._game_state == "BLACK_WON":
            return False

        # make move, clear any stones that may be on the edges
        board.move_piece(start_location, new_location)
        board.clear_edges()

        # if move leaves current player without a ring
        if self._player_turn not in board.ring_piece():
            return False

        # update turn to next player
        if self._player_turn == "WHITE":
            self._player_turn = "BLACK"
        elif self._player_turn == "BLACK":
            self._player_turn = "WHITE"

        # if opposing player has no ring, player wins
        if self._player_turn not in board.ring_piece():
            self.resign_game()

        # update game board
        self._board = board.get_board()

        return True

