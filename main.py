'''The chess frontend'''
from functools import partial
import tkinter as tk
import backend as bk


def select_char(color: int) -> str:
    '''Makes a window to select piece'''
    sel_char = ''
    but_chars = ['Q', 'R', 'B', 'N']

    def choose_char(char: str):
        nonlocal sel_char, top
        sel_char = char
        top.destroy()

    top = tk.Toplevel(win)
    top.geometry('240x90')
    top.title('child')
    frame = tk.Frame(master=top)

    col = 'w' if color == bk.WHITE else 'b'

    for i, x in enumerate(but_chars):
        icon = icons[col + x.lower()]
        cmd = partial(choose_char, x)
        tk.Button(master=frame, text=x, width=45, height=45, command=cmd, image=icon).grid(row=0, column=i)
    frame.pack(padx=15, pady=15)

    top.wait_window()

    return sel_char


def onclick(row, col):
    '''Calls on interaction with board in window'''
    global move
    if move is None:
        if board.get_piece(row, col) is not None:
            move = row, col
    else:
        piece = board.get_piece(*move)
        color = piece.get_color()
        if isinstance(piece, bk.Pawn) and \
           (color == bk.WHITE and row == 7) or (color == bk.BLACK and row == 0):
            char = select_char(color)
            board.move_and_promote_pawn(*move, row, col, char)
            move = None
            update()
            return

        board.move_piece(*move, row, col)
        move = None
    update()


def update():
    '''Re-draws the board'''
    if board.get_mate() is not None:
        top = tk.Toplevel(master=win)
        lbl = tk.Label(master=top, text='Check and mate')
        lbl.pack()
        top.wait_window()
        quit()
    bltext = 'Ходят ' + ('белые' if board.current_player_color() == bk.WHITE else 'черные')
    print('Check:', board.get_check())
    bl.config(text=bltext)
    for i in range(7, -1, -1):
        for j in range(8):
            type = (i + j + 1) % 2  # 0 is light, 1 is dark
            bg = ['burlywood1', 'burlywood3'][type]
            if move is not None:
                if board.can_move(*move, i, j):
                    bg = ['cyan2', 'cyan3'][type]
                if board.can_attack(*move, i, j):
                    bg = ['red', 'darkred'][type]
                if isinstance(board.get_piece(*move), bk.King):
                    if board.can_castle(*move, i, j):
                        bg = 'cyan'
            if move == (i, j):
                bg = 'green'

            cell = board.cell(i, j)
            img = icons[cell.lower()]
            buttons[i][j].config(bg=bg, image=img)


def get_image(char: str) -> tk.PhotoImage:
    '''Returns an image for asked code name'''
    if char == '  ':
        return holder
    return tk.PhotoImage(file=f'icons/{char.lower()}.png')


board = bk.Board()
win = tk.Tk()
win.title('PyChess (WIP)')

main_frame = tk.Frame(master=win, padx=10, pady=10, relief=tk.RAISED)
holder = tk.PhotoImage(width=45, height=45)

move = None

chars = ('wk', 'wq', 'wr', 'wb', 'wn', 'wp', 'bk', 'bq', 'br', 'bb', 'bn', 'bp')
icons = {'  ': holder}

for i in chars:
    icons[i] = get_image(i)

buttons = []

for i in range(7, -1, -1):
    buttons.append([])
    for j in range(8):
        bg = 'navajo white' if (i + j) % 2 else 'tan1'

        cmd = partial(onclick, 7 - i, j)
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
        buttons[len(buttons) - 1].append(but)


main_frame.pack()
bl = tk.Label(text='Chess', fg='black', padx=10, pady=10)
bl.pack()
update()

win.mainloop()
