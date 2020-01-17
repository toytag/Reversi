from ctypes import CDLL, Structure, c_uint8, c_float, byref

_libreversi = CDLL("./libreversi.so")

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
        res = _libreversi.put_chess(byref(self), x, y, player)
        return True if res == 1 else False

    def check_status(self):
        _libreversi.check_status(byref(self))

    def is_end(self):
        res = _libreversi.is_end(self)
        return True if res == 1 else False

    def minimax(self, depth, player):
        best_move = _libreversi.minimax_parallel(self, depth, player)
        return divmod(best_move, 8)