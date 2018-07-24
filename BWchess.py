import numpy as np

class BWchess():
    player_black = 1
    player_white = -1

    def __init__(self):
        self.chess_board = np.zeros((8, 8), dtype=np.int8)
        self.chess_board[3, 3], self.chess_board[4, 4] = -1, -1
        self.chess_board[3, 4], self.chess_board[4, 3] = 1, 1
        self.round_counter = 0

    def put_chess(self, x, y, identity):
        if self.chess_board[x, y] == 0:
            self.chess_board[x, y] = identity

            # put check
            condition = self.reverse_chess(x, y, identity)
            if condition:
                return True
            else:
                self.chess_board[x, y] = 0
                return False
                
        else:
            return False

    def reverse_chess(self, x, y, identity):
        # get related lines
        S = self.chess_board[:, y]
        H = self.chess_board[x, :]
        X = np.diag(self.chess_board, y - x)
        F = np.diag(self.chess_board[:, ::-1],(7 - y) - x)

        condition = False

        # reverse the chess
        for line in [S[:x][::-1], S[x+1:], H[:y][::-1], H[y+1:], \
                     X[:min(x, y)][::-1], X[min(x, y)+1:], \
                     F[:min(x, 7-y)][::-1], F[min(x, 7-y)+1:]]:

            # make np.array writeable when represented as line
            line.flags.writeable = True

            for i, chess in enumerate(line):
                if chess == 0:
                    break
                elif chess == identity:
                    if i == 0:
                        break
                    line[:i] = identity
                    condition = True
                    break

        return condition

    def check_winner(self):
        pass

if __name__ == "__main__":
    BWchess()
