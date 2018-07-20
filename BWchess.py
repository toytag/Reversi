import numpy as np

class BWchess():
    player_black = 1
    player_white = -1

    def __init__(self):
        self.chess_board = np.zeros((8, 8), dtype=np.int8)
        self.chess_board[3, 3], self.chess_board[4, 4] = 1, 1
        self.chess_board[3, 4], self.chess_board[4, 3] = -1, -1
        self.round_counter = 0

        # while True:
        #     coord = [int(i) for i in input().replace(' ', '')]
        #     # counter remain if coord is not available
        #     if self.put_chess(*coord, 1 if self.round_counter % 2 == 0 else -1):
        #         self.round_counter += 1
        #     print(self.chess_board)

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

        # feedback info for put check
        condition = False

        # reverse the chess
        for line in [S[:x][::-1], S[x+1:], H[:y][::-1], H[y+1:], \
                     X[:min(x, y)][::-1], X[min(x, y)+1:], \
                     F[:min(x, 7-y)][::-1], F[min(x, y-1)+1:]]:

            # make np.array writeable when represented as line
            line.flags.writeable = True

            for i, chess in enumerate(line):
                if chess == 0 and i == 0:
                    break
                elif chess == 0 and i > 1:
                    for j in range(1, i):
                        if line[i-j] == identity:
                            line[:i-j] = identity
                            condition = True
                    break

        return condition

    def check_winner(self):
        pass

if __name__ == "__main__":
    BWchess()
