class Board:
    def __init__(self):
        self.check = False
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self) -> int:
        return self.color

    def cell(self, row: int, col: int) -> str:
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row: int, col: int, row1: int, col1: int) -> bool:
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def is_under_attack(self, row: int, col: int, color: int) -> bool:
        for y in self.field:
            for piece in y:
                if piece is None:
                    continue
                if piece.get_color() != color:
                    continue
                if piece.can_move(row, col):
                    return True
        return False

    def get_piece(self, row: int, col: int) -> 'Piece':
        return self.field[row][col]

    def move_and_promote_pawn(self, row: int, col: int, row1: int, col1: int, char: int) -> bool:
        piece = self.get_piece(row, col)

        if piece is None:
            return False
        if not isinstance(piece, Pawn):
            return False
        if not piece.can_move(self, row, col, row1, col1) and not piece.can_attack(self, row, col, row1, col1):
            return False
        if not (piece.get_color() == WHITE and row1 == 7) and not (piece.get_color() == BLACK and row1 == 0):
            return False

        # https://pastebin.com/hmaJ5zDx
        color = piece.get_color()

        if char == 'Q':
            new_piece = Queen(color)
        elif char == 'R':
            new_piece = Rook(color)
        elif char == 'B':
            new_piece = Bishop(color)
        elif char == 'N':
            new_piece = Knight(color)

        self.field[row][col] = None
        self.field[row1][col1] = new_piece
        self.color = opponent(self.color)
        return True


class Piece:
    def __init__(self, color: int) -> None:
        self.color = color

    def set_position(self, row: int, col: int) -> None:
        if not correct_coords(row, col):
            return

        self.row = row
        self.col = col

    def get_color(self) -> int:
        return self.color

    def char(self) -> str:
        pass

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if board.current_player_color() != self.color:
            return False
        if not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if piece.get_color() == self.color:
                return False
        return True

    def can_attack(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if board.current_player_color() != self.color:
            return False
        if not correct_coords(row1, col1):
            return False
        if board.get_piece(row1, col1) is None:
            return False
        if row == row1 and col == col1:
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if piece.get_color() == self.color:
                return False
        return True


class Rook(Piece):
    def __init__(self, color: int) -> None:
        self.color = color

    def get_color(self) -> int:
        return self.color

    def char(self) -> str:
        return 'R'

    def can_move(self, board: int, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False
        return True

    def can_attack(self, board: int, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Pawn(Piece):
    def __init__(self, color: int) -> None:
        self.color = color

    def get_color(self) -> int:
        return self.color

    def char(self) -> str:
        return 'P'

    def can_move(self, board: int, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        if col != col1:
            return False

        if board.get_piece(row1, col1) is not None:
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board: int, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight(Piece):
    def __init__(self, color: int) -> None:
        super().__init__(color)

    def char(self) -> str:
        return 'N'

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        posr = abs(row - row1)
        posc = abs(col - col1)

        if sorted([posr, posc]) == [1, 2]:
            return True
        return False

    def can_attack(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):
    def __init__(self, color: int) -> None:
        super().__init__(color)

    def char(self) -> str:
        return 'B'

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        posr = row - row1
        posc = col - col1

        if abs(posr) != abs(posc):
            return False

        step_x = 1 if col < col1 else -1
        step_y = 1 if row < row1 else -1

        for i in range(1, abs(posr)):
            y = i * step_y + row
            x = i * step_x + col
            if not correct_coords(y, x):
                continue

            if board.get_piece(y, x) is not None:
                return False

        return True

    def can_attack(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):
    def __init__(self, color: int) -> None:
        super().__init__(color)

    def char(self) -> str:
        return 'Q'

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False

        if col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            return True

        if row == row1:
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True

        posr = row - row1
        posc = col - col1

        if abs(posr) == abs(posc):

            step_x = 1 if col < col1 else -1
            step_y = 1 if row < row1 else -1

            for i in range(1, abs(posr)):
                y = i * step_y + row
                x = i * step_x + col
                if not correct_coords(y, x):
                    continue

                if board.get_piece(y, x) is not None:
                    return False
            return True
        return False

    def can_attack(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class King(Piece):
    def __init__(self, color: int) -> None:
        super().__init__(color)

    def char(self) -> str:
        return 'K'

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        mx = abs(col - col1)
        my = abs(row - row1)
        if not mx in [0, 1]:
            return False
        if not my in [0, 1]:
            return False
        return True

    def can_attack(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)
        # TODO: "check" check
        # TODO: King class can_attack()


def opponent(color: int):
    if color == WHITE:
        return BLACK
    return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


def print_board(board):
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    board = Board()

    while True:
        print_board(board)

        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')

        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


if __name__ == '__main__':
    WHITE = 1
    BLACK = 2
    main()

WHITE = 1
BLACK = 2
