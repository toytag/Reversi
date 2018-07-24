import math
import tkinter as tk
from BWchess import BWchess

class BWchessEnv(tk.Tk):
    def __init__(self):
        # initialize BWchess
        self.chess = BWchess()

        # initialize tk
        super().__init__()
        self.title('Black & White Chess')
        self.geometry('400x400')
        self.__setup_canvas()

        # start window
        self.mainloop()

    def __setup_canvas(self):
        self.canvas = tk.Canvas(self, bg='Tan', width=400, height=400)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.__scheduler)
        self.__update_board()

    def __update_board(self):
        self.canvas.delete('all')

        for i in range(50, 400, 50):
            # vertical line
            self.canvas.create_line(i, 0, i, 400)
            # horizontal line
            self.canvas.create_line(0, i, 400, i)

        for i in range(8):
            for j in range(8):
                if self.chess.chess_board[i, j] != 0:
                    self.canvas.create_oval(j * 50 + 5, i * 50 + 5, \
                                            j * 50 + 45, i * 50 + 45, \
                                            fill='black' if self.chess.chess_board[i, j] == 1 else 'white')

        self.update()

    def __scheduler(self, event):
        # calculate coordinates and id
        x = math.floor(event.y / 50)
        y = math.floor(event.x / 50)
        identity = 1 if self.chess.round_counter % 2 == 0 else -1

        # put chess
        if self.chess.put_chess(x, y, identity):
            self.chess.round_counter += 1
            self.__update_board()
        

if __name__ == '__main__':
    BWchessEnv()