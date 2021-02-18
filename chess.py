import sys
from colorama import Fore, Style
from copy import deepcopy, copy


class Board:
    def __init__(self, board=None):
        if not board:
            self.board_init()
            self.print_board()
        else:
            self.board = board

    def board_init(self):
        """ Sets start values for board list """

        self.board = [
            list("8rnbqkbnr8"),
            list("7pppppppp7"),
            list("6••••••••6"),
            list("5••••••••5"),
            list("4••••••••4"),
            list("3••••••••3"),
            list("2PPPPPPPP2"),
            list("1RNBQKBNR1"),
        ]

    def print_board(self, moves=None):
        """ Prints board """

        print("╔═════════════════════╗")
        print("║   A B C D E F G H   ║")
        print("║ ╔═════════════════╗ ║")
        for i in range(0, 8):
            for j in range(0, 10):
                if j == 0 or j == 9:
                    print("║" + self.board[i][j] + "║", end=" ")
                else:
                    if moves is None:
                        if self.board[i][j].isupper():
                            print(Fore.RED + self.board[i][j], end=" ")
                        elif self.board[i][j].islower():
                            print(Fore.BLUE + self.board[i][j], end=" ")
                        else:
                            print(self.board[i][j], end=" ")
                    else:
                        if self.board[i][j].isupper():
                            if moves["kill"].count([i, j]) == 1:
                                print(Fore.GREEN + self.board[i][j], end=" ")
                            else:
                                print(Fore.RED + self.board[i][j], end=" ")
                        elif self.board[i][j].islower():
                            if moves["kill"].count([i, j]) == 1:
                                print(Fore.GREEN + self.board[i][j], end=" ")
                            else:
                                print(Fore.BLUE + self.board[i][j], end=" ")
                        else:
                            if moves["move"].count([i, j]) == 1:
                                print(Fore.GREEN + self.board[i][j], end=" ")
                            else:
                                print(self.board[i][j], end=" ")
                print(Style.RESET_ALL, end="")
            print()
        print("║ ╚═════════════════╝ ║")
        print("║   A B C D E F G H   ║")
        print("╚═════════════════════╝")

    def get_figure(self, coordinate) -> str:
        """ Gets figure in given coordinate """

        figure = self.board[coordinate.row][coordinate.column]
        return figure


class Coordinate:
    def __init__(self, coordinate: str or list):
        if type(coordinate) == str:
            coordinate = self.validate_str(coordinate)
            if coordinate:
                self.coordinate = coordinate
                self.row = self.parce_row()
                self.column = self.parce_column()
            else:
                self.coordinate = False
        else:
            if self.validate_list(coordinate):
                self.row = int(coordinate[0])
                self.column = int(coordinate[1])
                self.coordinate = self.parce_from_list()
            else:
                self.coordinate = False

    def validate_str(self, coordinate: str) -> str or bool:
        """ Validates str view of the coordinate """

        coordinate = coordinate.lower()
        if (
            ord(coordinate[0]) >= 97
            and ord(coordinate[0]) <= 104
            and ord(coordinate[1]) >= 49
            and ord(coordinate[1]) <= 56
        ):
            return coordinate
        else:
            return False

    def validate_list(self, coordinate: list) -> bool:
        """ Validates list view of the coordinate """

        if (
            coordinate[0] < 8
            and coordinate[0] >= 0
            and coordinate[1] <= 8
            and coordinate[1] >= 1
        ):
            return True
        else:
            return False

    def parce_row(self) -> int:
        """ Converts row number to the first index for Board obj """

        row = 8 - int(self.coordinate[1])
        return row

    def parce_column(self) -> int:
        """ Converts column letter to the second index for Board obj """

        column = ord(self.coordinate[0]) - 96
        return column

    def parce_from_list(self) -> str:
        """ Converts two indexes into a str view of the coordinate """

        str_row = str(8 - self.row)
        str_column = chr(96 + self.column)
        return str_column + str_row


class Figure:
    def __init__(self, name: str, color: str, coordinate: Coordinate):
        self.name = name
        self.color = color
        self.position = coordinate
        self.legal_moves = {"move": [], "kill": []}

    def get_moves(self):
        legal_moves_str = [move.coordinate for move in self.legal_moves["move"]]
        legal_kills_str = [move.coordinate for move in self.legal_moves["kill"]]
        all_moves_str = {"move": legal_moves_str, "kill": legal_kills_str}
        return all_moves_str

    def get_cheat_moves(self):
        legal_moves_str = [[move.row, move.column] for move in self.legal_moves["move"]]
        legal_kills_str = [[move.row, move.column] for move in self.legal_moves["kill"]]
        all_moves_str = {"move": legal_moves_str, "kill": legal_kills_str}
        return all_moves_str


class Pawn(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "P"
        else:
            name = "p"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        if self.color == "WHITE":
            if (
                self.board[self.position.row - 2][self.position.column] == "•"
                and self.position.row > 0
                and self.position.row == 6
            ):
                forward = Coordinate([self.position.row - 2, self.position.column])
                self.legal_moves["move"].append(forward)
            if (
                self.board[self.position.row - 1][self.position.column] == "•"
                and self.position.row > 0
            ):
                forward = Coordinate([self.position.row - 1, self.position.column])
                self.legal_moves["move"].append(forward)
            if (
                self.board[self.position.row - 1][self.position.column - 1].islower()
                and self.position.row > 0
                and self.position.column > 1
            ):
                left_eat = Coordinate([self.position.row - 1, self.position.column - 1])
                self.legal_moves["kill"].append(left_eat)
            if (
                self.board[self.position.row - 1][self.position.column + 1].islower()
                and self.position.row > 0
                and self.position.column < 8
            ):
                right_eat = Coordinate(
                    [self.position.row - 1, self.position.column + 1]
                )
                self.legal_moves["kill"].append(right_eat)
        else:
            if (
                self.board[self.position.row + 2][self.position.column] == "•"
                and self.position.row < 7
                and self.position.row == 1
            ):
                forward = Coordinate([self.position.row + 2, self.position.column])
                self.legal_moves["move"].append(forward)
            if (
                self.board[self.position.row + 1][self.position.column] == "•"
                and self.position.row < 7
            ):
                forward = Coordinate([self.position.row + 1, self.position.column])
                self.legal_moves["move"].append(forward)
            if (
                self.board[self.position.row + 1][self.position.column - 1].isupper()
                and self.position.row < 7
                and self.position.column > 1
            ):
                left_eat = Coordinate([self.position.row + 1, self.position.column - 1])
                self.legal_moves["kill"].append(left_eat)
            if (
                self.board[self.position.row + 1][self.position.column + 1].isupper()
                and self.position.row < 7
                and self.position.column < 8
            ):
                right_eat = Coordinate(
                    [self.position.row + 1, self.position.column + 1]
                )
                self.legal_moves["kill"].append(right_eat)


class Bishop(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "B"
        else:
            name = "b"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        check_x = copy(self.position.row) + 1
        check_y = copy(self.position.column) + 1
        while check_x <= 7 and check_y <= 8:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x += 1
            check_y += 1

        check_x = copy(self.position.row) - 1
        check_y = copy(self.position.column) - 1
        while check_x >= 0 and check_y > 0:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x -= 1
            check_y -= 1

        check_x = copy(self.position.row) - 1
        check_y = copy(self.position.column) + 1
        while check_x >= 0 and check_y <= 8:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x -= 1
            check_y += 1

        check_x = copy(self.position.row) + 1
        check_y = copy(self.position.column) - 1
        while check_x <= 7 and check_y > 0:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x += 1
            check_y -= 1


class Rook(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "R"
        else:
            name = "r"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        check_x = copy(self.position.row) + 1
        while check_x <= 7:
            if self.board[check_x][self.position.column] == "•":
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[check_x][self.position.column].islower()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[check_x][self.position.column].isupper()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x += 1

        check_x = copy(self.position.row) - 1
        while check_x >= 0:
            if self.board[check_x][self.position.column] == "•":
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[check_x][self.position.column].islower()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[check_x][self.position.column].isupper()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x -= 1

        check_y = copy(self.position.column) + 1
        while check_y <= 8:
            if self.board[self.position.row][check_y] == "•":
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[self.position.row][check_y].islower()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[self.position.row][check_y].isupper()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_y += 1

        check_y = copy(self.position.column) - 1
        while check_y > 0:
            if self.board[self.position.row][check_y] == "•":
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[self.position.row][check_y].islower()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[self.position.row][check_y].isupper()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_y -= 1


class Queen(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "Q"
        else:
            name = "q"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        check_x = copy(self.position.row) + 1
        while check_x <= 7:
            if self.board[check_x][self.position.column] == "•":
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[check_x][self.position.column].islower()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[check_x][self.position.column].isupper()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x += 1

        check_x = copy(self.position.row) - 1
        while check_x >= 0:
            if self.board[check_x][self.position.column] == "•":
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[check_x][self.position.column].islower()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[check_x][self.position.column].isupper()
            ):
                legal_move = Coordinate([check_x, self.position.column])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x -= 1

        check_y = copy(self.position.column) + 1
        while check_y <= 8:
            if self.board[self.position.row][check_y] == "•":
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[self.position.row][check_y].islower()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[self.position.row][check_y].isupper()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_y += 1

        check_y = copy(self.position.column) - 1
        while check_y > 0:
            if self.board[self.position.row][check_y] == "•":
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["move"].append(legal_move)
            elif (
                self.color == "WHITE"
                and self.board[self.position.row][check_y].islower()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif (
                self.color == "BLACK"
                and self.board[self.position.row][check_y].isupper()
            ):
                legal_move = Coordinate([self.position.row, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_y -= 1

        check_x = copy(self.position.row) + 1
        check_y = copy(self.position.column) + 1
        while check_x <= 7 and check_y <= 8:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x += 1
            check_y += 1

        check_x = copy(self.position.row) - 1
        check_y = copy(self.position.column) - 1
        while check_x >= 0 and check_y > 0:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x -= 1
            check_y -= 1

        check_x = copy(self.position.row) - 1
        check_y = copy(self.position.column) + 1
        while check_x >= 0 and check_y <= 8:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x -= 1
            check_y += 1

        check_x = copy(self.position.row) + 1
        check_y = copy(self.position.column) - 1
        while check_x <= 7 and check_y > 0:
            if self.board[check_x][check_y] == "•":
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["move"].append(legal_move)
            elif self.color == "WHITE" and self.board[check_x][check_y].islower():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            elif self.color == "BLACK" and self.board[check_x][check_y].isupper():
                legal_move = Coordinate([check_x, check_y])
                self.legal_moves["kill"].append(legal_move)
                break
            else:
                break
            check_x += 1
            check_y -= 1


class King(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "K"
        else:
            name = "k"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        count_x = -1
        for i in range(3):
            if self.position.row + count_x >= 0 and self.position.row + count_x < 8:
                figure_check = self.board[self.position.row + count_x][
                    self.position.column - 1
                ]
                if figure_check == "•":
                    legal_move = Coordinate(
                        [self.position.row + count_x, self.position.column - 1]
                    )
                    self.legal_moves["move"].append(legal_move)
                else:
                    if self.color == "WHITE" and figure_check.islower():
                        legal_move = Coordinate(
                            [self.position.row + count_x, self.position.column - 1]
                        )
                        self.legal_moves["kill"].append(legal_move)
                    elif self.color == "BLACK" and figure_check.isupper():
                        legal_move = Coordinate(
                            [self.position.row + count_x, self.position.column - 1]
                        )
                        self.legal_moves["kill"].append(legal_move)
                count_x += 1

        count_x = -1
        for i in range(3):
            if self.position.row + count_x >= 0 and self.position.row + count_x < 8:
                figure_check = self.board[self.position.row + count_x][
                    self.position.column + 1
                ]
                if figure_check == "•":
                    legal_move = Coordinate(
                        [self.position.row + count_x, self.position.column + 1]
                    )
                    self.legal_moves["move"].append(legal_move)
                else:
                    if self.color == "WHITE" and figure_check.islower():
                        legal_move = Coordinate(
                            [self.position.row + count_x, self.position.column + 1]
                        )
                        self.legal_moves["kill"].append(legal_move)
                    elif self.color == "BLACK" and figure_check.isupper():
                        legal_move = Coordinate(
                            [self.position.row + count_x, self.position.column + 1]
                        )
                        self.legal_moves["kill"].append(legal_move)
                count_x += 1

        if self.position.row + 1 < 8:
            figure_check = self.board[self.position.row + 1][self.position.column]
            if figure_check == "•":
                legal_move = Coordinate([self.position.row + 1, self.position.column])
                self.legal_moves["move"].append(legal_move)
            else:
                if self.color == "WHITE" and figure_check.islower():
                    legal_move = Coordinate(
                        [self.position.row + 1, self.position.column]
                    )
                    self.legal_moves["kill"].append(legal_move)
                elif self.color == "BLACK" and figure_check.isupper():
                    legal_move = Coordinate(
                        [self.position.row + 1, self.position.column]
                    )
                    self.legal_moves["kill"].append(legal_move)

        if self.position.row - 1 >= 0:
            figure_check = self.board[self.position.row - 1][self.position.column]
            if figure_check == "•":
                legal_move = Coordinate([self.position.row - 1, self.position.column])
                self.legal_moves["move"].append(legal_move)
            else:
                if self.color == "WHITE" and figure_check.islower():
                    legal_move = Coordinate(
                        [self.position.row - 1, self.position.column]
                    )
                    self.legal_moves["kill"].append(legal_move)
                elif self.color == "BLACK" and figure_check.isupper():
                    legal_move = Coordinate(
                        [self.position.row - 1, self.position.column]
                    )
                    self.legal_moves["kill"].append(legal_move)


class Knight(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "N"
        else:
            name = "n"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        x = self.position.row
        y = self.position.column
        knight_list = [
            [x + 1, y + 2],
            [x - 1, y + 2],
            [x + 1, y - 2],
            [x - 1, y - 2],
            [x + 2, y + 1],
            [x - 2, y + 1],
            [x + 2, y - 1],
            [x - 2, y - 1],
        ]
        for i in knight_list:
            if i[0] < 8 and i[0] >= 0 and i[1] > 0 and i[1] <= 8:
                figure_check = self.board[i[0]][i[1]]
                if figure_check == "•":
                    legal_move = Coordinate([i[0], i[1]])
                    self.legal_moves["move"].append(legal_move)
                else:
                    if self.color == "WHITE" and figure_check.islower():
                        legal_move = Coordinate([i[0], i[1]])
                        self.legal_moves["kill"].append(legal_move)
                    elif self.color == "BLACK" and figure_check.isupper():
                        legal_move = Coordinate([i[0], i[1]])
                        self.legal_moves["kill"].append(legal_move)


class Cheat_move(Board):
    def __init__(self, cor: Coordinate, board: list, color: str):
        Board.__init__(self, board)
        self.cor = cor
        self.color = color
        self.figure = None
        self.set_figure()

    def set_figure(self):
        """ Sets figure wich stands in the from coordinate """

        figure_name = self.get_figure(self.cor).lower()
        if figure_name == "p":
            self.figure = Pawn(self.color, self.cor, self.board)
        elif figure_name == "b":
            self.figure = Bishop(self.color, self.cor, self.board)
        elif figure_name == "r":
            self.figure = Rook(self.color, self.cor, self.board)
        elif figure_name == "q":
            self.figure = Queen(self.color, self.cor, self.board)
        elif figure_name == "k":
            self.figure = King(self.color, self.cor, self.board)
        else:
            self.figure = Knight(self.color, self.cor, self.board)


class Move(Board):
    def __init__(
        self, from_cor: Coordinate, to_cor: Coordinate, board: list, color: str
    ):
        Board.__init__(self, board)
        self.from_cor = from_cor
        self.to_cor = to_cor
        self.color = color
        self.figure = None

    def check_from_cor(self) -> bool:
        """ Checks if the start position has a figure on it """

        figure = self.get_figure(self.from_cor)

        if figure != "•":
            if (
                figure.isupper()
                and self.color == "WHITE"
                or figure.islower()
                and self.color == "BLACK"
            ):
                return True
        else:
            return False

    def cheat_get_moves(self, flag):
        if flag is None:
            return None
        else:
            return self.figure.get_moves()

    def check_to_cor(self, moves: list) -> bool:
        """ Checks if the to coordinate is in the legal moves list of the figure that is chosen """

        if (
            moves["move"].count(self.to_cor.coordinate) == 1
            or moves["kill"].count(self.to_cor.coordinate) == 1
        ):
            return True
        else:
            return False

    def validate_move(self) -> bool:
        """ Checks if the given move is legal """

        if self.check_from_cor():
            self.set_figure()
            moves = self.figure.get_moves()
            if self.check_to_cor(moves):
                return True
            else:
                print(f"Illegal move for figure {self.figure.name}")
                return False
        else:
            print("No figure on the first coordinate or you've chozen oponent's figure")
            return False

    def game_over(self):
        print(f"{self.color} - won!")
        sys.exit(1)

    def make_move(self):
        """ Changes figure position on bard """

        self.board[self.from_cor.row][self.from_cor.column] = "•"
        if self.board[self.to_cor.row][self.to_cor.column].lower() == "k":
            self.game_over()
        else:
            self.board[self.to_cor.row][self.to_cor.column] = self.figure.name

    def set_figure(self):
        """ Sets figure wich stands in the from coordinate """

        figure_name = self.get_figure(self.from_cor).lower()
        if figure_name == "p":
            self.figure = Pawn(self.color, self.from_cor, self.board)
        elif figure_name == "b":
            self.figure = Bishop(self.color, self.from_cor, self.board)
        elif figure_name == "r":
            self.figure = Rook(self.color, self.from_cor, self.board)
        elif figure_name == "q":
            self.figure = Queen(self.color, self.from_cor, self.board)
        elif figure_name == "k":
            self.figure = King(self.color, self.from_cor, self.board)
        else:
            self.figure = Knight(self.color, self.from_cor, self.board)


class Gameplay:
    def __init__(self):
        """ Sets status, draws a board """

        self.status = "WHITE"
        self.moves = 1
        self.board = Board()
        self.game_process()

    def change_status(self):
        if self.status == "WHITE":
            self.status = "BLACK"
        else:
            self.status = "WHITE"
            self.moves += 1  # Increase moves counter only on the move of whites

    def show_moves(self):
        print(f"The number of moves  -  {self.moves}.")

    def print_instructions(self):
        print(
            """

                        Welcome to the game of chess!!!
                                Instructions:
        1) If you want to exit just type 'exit'
        2) To make a move you need to type in coordinate of the figure that 
           needs to be moved, space and a coordinate of where you want your
           figure to move. For example: 'a2 a3' or 'F2 H3'
        3) If you want to see how many moves were made, type in 'moves'
        4) If you want to read instruction again, type in 'instruction'
        5) If you want to see all possible moves for your figure - type in 'cheat', 
           then type in the coordinate of the your figure that needs to be checked

        """
        )

    def player_input(self) -> str:
        """ Gets an input from a player """

        if self.status == "WHITE":
            inp = str(input("Move for white!\n"))
        else:
            inp = str(input("Move for black!\n"))

        return inp

    def cheat_get(self) -> str:
        print("Enter coordinates of your figure that you want to cheat with:")
        inp = str(input("->"))
        if len(inp) == 2:
            cor = Coordinate(inp)
        return cor

    def process_input(self, inp: str) -> list or bool:
        """ Converts input to list of coordinates, checks for 'exit' """

        def exit_chess():
            print("Bye bye")
            sys.exit(1)

        def wrong_input():
            print("Please check the format of your input and try again")
            return False

        def check_coordinates(coordinates: list) -> bool:
            """ Checks if coordinates are in the right format """

            if len(coordinates[0]) == 2 and len(coordinates[0]) == 2:
                return True
            else:
                return False

        if inp == "exit":
            exit_chess()
        elif inp == "moves":
            self.show_moves()
            return False
        elif inp == "instruction":
            self.print_instructions()
            return False

        try:
            coordinates = inp.split(" ")
            if (
                len(coordinates) == 2
                and len(inp) == 5
                and check_coordinates(coordinates)
            ):
                from_cor = Coordinate(coordinates[0])
                to_cor = Coordinate(coordinates[1])
                if (
                    from_cor.coordinate
                    and to_cor.coordinate
                    and from_cor.coordinate != to_cor.coordinate
                ):
                    return from_cor, to_cor
                else:
                    return wrong_input()
            else:
                return wrong_input()
        except:
            return wrong_input()

    def game_process(self):
        """ Main game process """

        self.print_instructions()
        while True:
            self.cheat = None
            inp = self.player_input()
            if inp == "cheat":
                cor = self.cheat_get()
                cheat_move = Cheat_move(cor, self.board.board, self.status)
                print(cheat_move.figure.get_cheat_moves())
                self.board.print_board(cheat_move.figure.get_cheat_moves())
                continue

            coordinates = self.process_input(inp)
            if coordinates:  # Coordinates are writen in the right format
                move = Move(
                    coordinates[0], coordinates[1], self.board.board, self.status
                )
                if move.validate_move():  # Move can be done
                    move.make_move()
                    self.board.print_board()
                    self.change_status()
            else:
                pass


Gameplay()
