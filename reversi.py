import platform
from ctypes import CDLL, Structure, c_uint8, c_float, c_bool, byref

if platform.system() == 'Linux':
    _libreversi = CDLL("./lib/libreversi.so")
elif platform.system() == 'Darwin':
    _libreversi = CDLL("./lib/libreversi.dylib")
elif platform.system() == 'Windows':
    _libreversi = CDLL("./lib/libreversi.dll")
else:
    print('please compile from source')
    exit(0)

_libreversi.put_chess.restype = c_bool
_libreversi.is_end.restype = c_bool

class REVERSI(Structure):
    _fields_ = [
        ("chess_board", (c_uint8 * 8) * 8),
        ("avl_board", (c_uint8 * 8) * 8),
        ("black_count", c_uint8),
        ("black_avl_count", c_uint8),
        ("white_count", c_uint8),
        ("white_avl_count", c_uint8),
        ("round_count", c_uint8)
    ]

class reversi(REVERSI):
    EMPTY = c_uint8.in_dll(_libreversi, "EMPTY").value
    BLACK = c_uint8.in_dll(_libreversi, "BLACK").value
    WHITE = c_uint8.in_dll(_libreversi, "WHITE").value
    BOTH  = c_uint8.in_dll(_libreversi, "BOTH").value

    def __init__(self):
        _libreversi.init(byref(self))

    def put_chess(self, x, y, player):
        return _libreversi.put_chess(byref(self), x, y, player)

    def check_status(self):
        _libreversi.check_status(byref(self))

    def is_end(self):
        return _libreversi.is_end(self)

    def minimax(self, depth, player):
        best_move = _libreversi.minimax_parallel(self, depth, player)
        return divmod(best_move, 8)

def print_board(board):
    for i in range(8):
        for j in range(8):
            print(board[i][j], end=' ')
        print()

def inspect(env):
    print()
    print("chess_board:")
    print_board(env.chess_board)
    print("avl_board:")
    print_board(env.avl_board)
    print(f"black_count:\t {env.black_count}")
    print(f"black_avl_count: {env.black_avl_count}")
    print(f"white_count:\t {env.white_count}")
    print(f"white_avl_count: {env.white_avl_count}")
    print(f"round_count:\t {env.round_count}")
    print()

if __name__ == "__main__":
    # run test
    env = reversi()

    skip_count = 0

    while not env.is_end():
        player = reversi.BLACK if env.round_count % 2 == 0 else reversi.WHITE
        best_move = env.minimax(4, player)
        if best_move == (3, 3):
            skip_count += 1
        env.put_chess(*best_move, player)
        env.check_status()

    inspect(env)

    assert env.black_count + env.white_count - 4 + skip_count == env.round_count
    print("python test success!")