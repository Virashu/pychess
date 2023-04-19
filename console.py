import backend as bk


board = bk.Board()

def print_board(board: bk.Board) -> None:
    pieces = {♔
♕
♖
♗
♘
♙
♚
♛
♜
♝
♞
Шахматная фигура черная пешка
}

while not board.mate:
    # board.update()

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