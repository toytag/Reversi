import math
import tkinter as tk
from tkinter import messagebox
from reversi import reversi


class reversiGUI(tk.Tk):
    def __init__(self):
        # initialize reversi
        self.chess = reversi()

        # initialize tk
        super().__init__()
        self.title('Reversi')
        self.geometry('400x400')
        self.__setup_canvas()

        # start window
        self.mainloop()

    def __setup_canvas(self):
        self.canvas = tk.Canvas(self, bg='BurlyWood', width=400, height=400)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.__scheduler)
        for i in range(50, 400, 50):
            # the vertical line
            self.canvas.create_line(i, 0, i, 400)
            # the horizontal line
            self.canvas.create_line(0, i, 400, i)
        self.__update_board()

    def __update_board(self):
        self.canvas.delete('chess', 'avai')

        player = reversi.BLACK \
            if self.chess.round_count % 2 == 0 else reversi.WHITE

        for i in range(8):
            for j in range(8):
                if self.chess.avl_board[i, j] in [player, reversi.BOTH]:
                    self.canvas.create_oval(
                        j * 50 + 20, i * 50 + 20,
                        j * 50 + 30, i * 50 + 30,
                        outline='cyan',
                        fill='cyan',
                        tags='avai',
                    )
                if self.chess.chess_board[i, j] != 0:
                    self.canvas.create_oval(
                        j * 50 + 5, i * 50 + 5,
                        j * 50 + 45, i * 50 + 45,
                        fill={
                            reversi.BLACK: 'black',
                            reversi.WHITE: 'white',
                        }.get(self.chess.chess_board[i, j]),
                        tags='chess',
                    )
                    
        self.update()

    def __scheduler(self, event):
        # calculate coordinates and player
        x = math.floor(event.y / 50)
        y = math.floor(event.x / 50)
        player = reversi.BLACK \
            if self.chess.round_count % 2 == 0 else reversi.WHITE

        # put chess
        if self.chess.put_chess(x, y, player):
            self.chess.check_status()
            self.__update_board()

            # for GUI, now moved to reversiGui.py
            # Game end
            if self.chess.black_avl_count == 0 and self.chess.white_avl_count == 0:
                if self.chess.black_count > self.chess.white_count:
                    messagebox.showinfo('Reversi',
                        f'Black Win\n\n{self.chess.black_count} : {self.chess.white_count}')
                elif self.chess.black_count < self.chess.white_count:
                    messagebox.showinfo('Reversi',
                        f'White Win\n\n{self.chess.black_count} : {self.chess.white_count}')
                else:
                    messagebox.showinfo('Reversi', 'Tie')
                self.destroy()
                exit()
                
        self.__update_board()
        

if __name__ == '__main__':
    reversiGUI()