import backend as bk
import tkinter as tk


# Усл. обозначения фигур в программе и их символы в NerdFont
chess = {'K': '󰡗', 'Q': '󰡚', 'B': '', 'N': '', 'R': '', 'P': ''}

win = tk.Tk()

for i in range(8):
    for j in range(8):
        bg = 'white' if (i + j) % 2 else 'black'
        frame = tk.Frame(
            master=win,
            relief=tk.RAISED,
            borderwidth=1,
            bg=bg
        )
        frame.grid(row=i, col=j)
        label = tk.Label(master=frame, text=f'{chess["K"]}')
        label.pack()


# board = bk.Board()

# bk.main()
