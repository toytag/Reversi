import numpy as np
from scipy.signal import convolve2d


class reversi:
    BLACK = 1
    WHITE = 2
    BOTH = 3

    def __init__(self):
        # initialization
        self.chess_board = np.zeros((8, 8), dtype=np.int8)
        self.avl_board = np.zeros((8, 8), dtype=np.int8)
        self.black_count, self.black_avl_count = 0, 0
        self.white_count, self.white_avl_count = 0, 0
        self.round_count = 0
        # initial status for the game
        self.chess_board[3, 3], self.chess_board[4, 4] = reversi.WHITE, reversi.WHITE
        self.chess_board[3, 4], self.chess_board[4, 3] = reversi.BLACK, reversi.BLACK
        # inital check
        self.check_status()

    def put_chess(self, x, y, player):
        # check if player has available position
        avai_count = {
            reversi.BLACK: self.black_avl_count,
            reversi.WHITE: self.white_avl_count,
        }.get(player)
        if avai_count == 0:
            self.round_count += 1
            return True
        # check if x, y is one of the available position
        if self.avl_board[x, y] in [player, reversi.BOTH]:
            self.chess_board[x, y] = player
            self.flip(x, y, player)
            self.round_count += 1
            return True
        else:
            return False

    def flip(self, x, y, player, check=False):
        # if check is True, return True or False and don't change chess_board
        # if check is False, flip the chess and return None

        # get related lines
        vertical = self.chess_board[:, y]
        horizontal = self.chess_board[x, :]
        slash = np.diag(self.chess_board, y-x)
        backslash = np.diag(self.chess_board[:, ::-1], (7-y)-x)

        # flip the chess
        for line in [
            vertical[:x][::-1], vertical[x+1:],
            horizontal[:y][::-1], horizontal[y+1:],
            slash[:min(x, y)][::-1], slash[min(x, y)+1:],
            backslash[:min(x, 7-y)][::-1], backslash[min(x, 7-y)+1:],
        ]:
            for i, chess in enumerate(line):
                if chess == 0:
                    break
                elif chess == player:
                    if i != 0:
                        if check:
                            return True
                        # make np.array writeable when represented as `line`
                        line.flags.writeable = True
                        line[:i] = player
                    break
        
        if check:
            return False

    def check_status(self):
        # reset
        self.avl_board = np.zeros((8, 8), dtype=np.int8)
        self.black_count, self.black_avl_count = 0, 0
        self.white_count, self.white_avl_count = 0, 0

        # use convolution to determine whether one position should be checked
        check_board = convolve2d(self.chess_board, np.ones((3, 3)), mode='same')
        for i, j in zip(*check_board.nonzero()):
            if self.chess_board[i, j] == reversi.BLACK:
                self.black_count += 1
            elif self.chess_board[i, j] == reversi.WHITE:
                self.white_count += 1
            else:
                if self.flip(i, j, reversi.BLACK, check=True):
                    self.avl_board[i, j] = reversi.BLACK
                    self.black_avl_count += 1
                if self.flip(i, j, reversi.WHITE, check=True):
                    self.avl_board[i, j] = reversi.WHITE \
                        if self.avl_board[i, j] == 0 else reversi.BOTH
                    self.white_avl_count += 1
