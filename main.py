import backend as bk
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial


def choose_char(char: str):
    ...


def select_char(color: int) -> str:
    # TODO: Make popup window with type selection
    top = tk.Toplevel(win)
    top.geometry('200x200')
    top.title('child')
    but_chrs = ['Q', 'R', 'B', 'N']

    for i in but_chrs:
        cmd = partial(choose_char, )
        tk.Button(master=top, text=i, width=10, height=10, command=cmd)
    color_char = 'w' if color == bk.WHITE else 'b'
    return 'Q'  # FIXME


def onclick(row, col):
    global move
    if move is None:
        if board.get_piece(row, col) is not None:
            move = row, col
    else:
        piece = board.get_piece(*move)
        if isinstance(piece, bk.Pawn):
            color = piece.get_color()
            if (color == bk.WHITE and row == 7) or (color == bk.BLACK and row == 0):
                char = select_char(color)
                board.move_and_promote_pawn(*move, row, col, char)
                move = None
                update()
                return

        res = board.move_piece(*move, row, col)
        print(res)  # FIXME
        move = None
    update()


def update():
    for i in range(8):
        for j in range(8):
            type = (i + j) % 2  # 0 is light, 1 is dark
            bg = ['burlywood1', 'burlywood3'][type]
            if move is not None:
                if board.get_piece(*move).can_move(board, *move, i, j):
                    # bg = ['goldenrod', 'dark goldenrod'][type]
                    bg = ['cyan2', 'cyan3'][type]
                if board.get_piece(*move).can_attack(board, *move, i, j):
                    bg = ['red', 'darkred'][type]
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
