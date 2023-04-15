import backend as bk
import tkinter as tk
from tkinter import font

# meslolgs = font.Font('MesloLGS NF')

# Усл. обозначения фигур в программе и их символы в NerdFont
chess = {'K': '󰡗', 'Q': '󰡚', 'B': '', 'N': '', 'R': '', 'P': ''}

win = tk.Tk()
main_frame = tk.Frame(master=win)
pixel = tk.PhotoImage(width=1, height=1)

def onclick(row, col):
    print(row, col)


for i in range(8):
    for j in range(8):
        bg = 'white' if (i + j) % 2 else 'black'
        frame = tk.Frame(
            master=main_frame,
            relief=tk.RAISED,
            borderwidth=1,
            bg=bg,
            height=40,
            width=40
        )
        frame.grid(row=i, column=j)
        but = tk.Button(
            master=frame,
            width=40,
            height=40,
            bg=bg,
            image=pixel,
            command=lambda: onclick()
        )
        but.pack()
        # label = tk.Label(master=frame, text=f'{chess["K"]}')
        # label = tk.Label(master=frame, text=f'', width=2, height=2)
        # label.pack()

bl = tk.Label()

main_frame.pack()
win.mainloop()

# board = bk.Board()

# bk.main()
