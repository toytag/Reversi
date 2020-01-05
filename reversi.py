import numpy as np


class reversi:
    player_black = 1
    player_white = -1

    def __init__(self):
        self.chess_board = np.zeros((8, 8), dtype=np.int8)
        self.available = np.zeros((8, 8), dtype=np.int8)
        self.chess_board[3, 3], self.chess_board[4, 4] = -1, -1
        self.chess_board[3, 4], self.chess_board[4, 3] = 1, 1
        self.round_counter = 0
        self.check_status()

    def put_chess(self, x, y, identity):
        if self.available[x, y] in [identity, 2]:
            self.chess_board[x, y] = identity
            self.flip(x, y, identity, check=False)
            self.available = np.zeros((8, 8), dtype=np.int8)
            return True
        else:
            return False

    def flip(self, x, y, identity, check=False):
        # if check is on return True or False and don't change chess_board
        # if check is off flip the chess and return None

        # get related lines
        S = self.chess_board[:, y]
        H = self.chess_board[x, :]
        X = np.diag(self.chess_board, y - x)
        F = np.diag(self.chess_board[:, ::-1],(7 - y) - x)

        condition = False

        # reverse the chess
        for line in [
            S[:x][::-1], S[x+1:], H[:y][::-1], H[y+1:],
            X[:min(x, y)][::-1], X[min(x, y)+1:],
            F[:min(x, 7-y)][::-1], F[min(x, 7-y)+1:]
        ]:
            # make np.array writeable when represented as line
            line.flags.writeable = True

            for i, chess in enumerate(line):
                if chess == 0:
                    break
                elif chess == identity:
                    if i == 0:
                        break
                    if check == False:
                        line[:i] = identity
                    condition = True
                    break

        if check == True:
            return condition

    def check_status(self):
        black_count = 0
        white_count = 0
        black_available = 0
        white_available = 0

        for i in range(8):
            for j in range(8):
                if self.chess_board[i, j] == self.player_black:
                    black_count += 1
                elif self.chess_board[i, j] == self.player_white:
                    white_count += 1
                else:
                    if self.flip(i, j, self.player_black, check=True):
                        self.available[i, j] = 1
                        black_available += 1
                    if self.flip(i, j, self.player_white, check=True):
                        if self.available[i, j] == 1:
                            self.available[i, j] = 2
                        else:
                            self.available[i, j] = -1
                        white_available += 1

        if black_available == 0 and white_available == 0:
            if black_count > white_count:
                return f'Black Win\n\n{black_count} : {white_count}'
            elif black_count < white_count:
                return f'White Win\n\n{black_count} : {white_count}'
            else:
                return 'Tie'
        elif black_available == 0:
            return 'black skip'
        elif white_available == 0:
            return 'white skip'
        else:
            return 'normal'


if __name__ == "__main__":
    reversi()