import tkinter as tk
from tkinter import messagebox
from reversi import reversi
from math import floor


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
        self.canvas.delete('chess', 'avl')

        player = reversi.BLACK \
            if self.chess.round_count % 2 == 0 else reversi.WHITE

        for i in range(8):
            for j in range(8):
                # important !!!
                # if the board doesn't show any available position,
                # it means that you don't have an available position to put chess,
                # continue to next round by clicking anywhere on the chess board
                if self.chess.avl_board[i][j] in [player, reversi.BOTH]:
                    self.canvas.create_oval(
                        j * 50 + 20, i * 50 + 20,
                        j * 50 + 30, i * 50 + 30,
                        outline='cyan',
                        fill='cyan',
                        tags='avl',
                    )
                if self.chess.chess_board[i][j] != 0:
                    self.canvas.create_oval(
                        j * 50 + 5, i * 50 + 5,
                        j * 50 + 45, i * 50 + 45,
                        fill='black' \
                            if self.chess.chess_board[i][j] == reversi.BLACK \
                            else 'white',
                        tags='chess',
                    )
                    
        self.update()

    def __scheduler(self, event):
        # calculate coordinates and player
        x = floor(event.y / 50)
        y = floor(event.x / 50)

        # put chess
        if self.chess.put_chess(x, y, reversi.BLACK):
            self.chess.check_status()
            self.__update_board()

            # for GUI, now moved to reversiGui.py
            # game over
            if self.chess.is_end():
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

            # bug !!!!!!!!!!!
            move = self.chess.minimax(depth=7, player=reversi.WHITE)

            self.chess.put_chess(*move, reversi.WHITE)
            self.chess.check_status()
            self.__update_board()

            # for GUI, now moved to reversiGui.py
            # game over
            if self.chess.is_end():
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