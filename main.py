import backend as bk
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial


def onclick(row, col):
    global move
    if move is None:
        move = row, col
    else:
        print(board.move_piece(*move, row, col))
        move = None
    update()


def update():
    for i in range(8):
        for j in range(8):
            bg = 'navajo white' if (i + j) % 2 else 'tan1'
            if move == (i, j):
                bg = 'green'

            cell = board.cell(i, j)
            img = icons[cell.lower()]
            buttons[i][j].config(bg=bg, image=img)
            # print(pieces[cell], end='')
        # print()


def get_image(char: str) -> ImageTk.PhotoImage:
    if char == '  ':
        return holder
    # return ImageTk.PhotoImage(Image.open(f'icons/{char.lower()}.png'))
    return tk.PhotoImage(file=f'icons/{char.lower()}.png')



board = bk.Board()
win = tk.Tk()
win.title('PyChess (WIP)')

main_frame = tk.Frame(master=win, padx=10, pady=10, relief=tk.RAISED)
holder = tk.PhotoImage(width=45, height=45)

move = None
# pieces = {
#     'wK': '♔',
#     'wQ': '♕',
#     'wR': '♖',
#     'wB': '♗',
#     'wN': '♘',
#     'wP': '♙',
#     'bK': '♚',
#     'bQ': '♛',
#     'bR': '♜',
#     'bB': '♝',
#     'bN': '♞',
#     'bP': '♟︎',
#     '  ': ' '
# }
chars = ('wk', 'wq', 'wr', 'wb', 'wn', 'wp', 'bk', 'bq', 'br', 'bb', 'bn', 'bp')
icons = {'  ': holder}

for i in chars:
    icons[i] = get_image(i)
print(icons)

buttons = []

for i in range(8):
    buttons.append([])
    for j in range(8):
        bg = 'navajo white' if (i + j) % 2 else 'tan1'

        cmd = partial(onclick, i, j)
        but = tk.Button(
            master=main_frame,
            # width=40,
            # height=40,
            bg=bg,
            image=holder,
            command=cmd,
            relief=tk.FLAT,
            text='ld'
        )
        but.grid(row=i, column=j)
        buttons[i].append(but)




main_frame.pack()
update()
bl = tk.Label(text='Chess', fg='black', padx=10, pady=10)
bl.pack()

win.mainloop()

# board = bk.Board()

# bk.main()
