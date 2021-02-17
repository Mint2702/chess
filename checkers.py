import sys
from colorama import Fore, Style


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
            list("8•B•B•B•B8"),
            list("7B•B•B•B•7"),
            list("6•B•B•B•B6"),
            list("5••••••••5"),
            list("4••••••••4"),
            list("3W•W•W•W•3"),
            list("2•W•W•W•W2"),
            list("1W•W•W•W•1"),
        ]

    def print_board(self):
        """ Prints board """

        print("╔═════════════════════╗")
        print("║   A B C D E F G H   ║")
        print("║ ╔═════════════════╗ ║")
        for i in range(0, 8):
            for j in range(0, 10):
                if j == 0 or j == 9:
                    print("║" + self.board[i][j] + "║", end=" ")
                else:
                    if self.board[i][j] == "B":
                        print(Fore.RED + self.board[i][j], end=" ")
                    elif self.board[i][j] == "W":
                        print(Fore.BLUE + self.board[i][j], end=" ")
                    elif self.board[i][j] == "•":
                        if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                            print(self.board[i][j], end=" ")
                        else:
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


class Checker(Figure, Board):
    def __init__(self, color: str, coordinate: Coordinate, board: Board):
        Board.__init__(self, board)
        if color == "WHITE":
            name = "W"
        else:
            name = "B"
        Figure.__init__(self, name, color, coordinate)
        self.set_moves()

    def set_moves(self):
        if self.color == "WHITE":
            if (
                self.board[self.position.row - 1][self.position.column - 1] == "•"
                and self.position.row > 0
                and self.position.column > 0
            ):
                forward_left = Coordinate(
                    [self.position.row - 1, self.position.column - 1]
                )
                self.legal_moves["move"].append(forward_left)
            if (
                self.board[self.position.row - 1][self.position.column + 1] == "•"
                and self.position.row > 0
                and self.position.column < 8
            ):
                forward_right = Coordinate(
                    [self.position.row - 1, self.position.column + 1]
                )
                self.legal_moves["move"].append(forward_right)
            if (
                self.board[self.position.row - 1][self.position.column - 1] == "B"
                and self.position.row > 1
                and self.position.column > 1
                and self.board[self.position.row - 2][self.position.column - 2] == "•"
            ):
                forward_left_eat = Coordinate(
                    [self.position.row - 1, self.position.column - 1]
                )
                self.legal_moves["kill"].append(forward_left_eat)
            if (
                self.board[self.position.row - 1][self.position.column + 1] == "B"
                and self.position.row > 1
                and self.position.column < 7
                and self.board[self.position.row - 2][self.position.column + 2] == "•"
            ):
                forward_right_eat = Coordinate(
                    [self.position.row - 1, self.position.column + 1]
                )
                self.legal_moves["kill"].append(forward_right_eat)
            if (
                self.board[self.position.row + 1][self.position.column - 1] == "B"
                and self.position.row < 6
                and self.position.column > 1
                and self.board[self.position.row + 2][self.position.column - 2] == "•"
            ):
                back_left_eat = Coordinate(
                    [self.position.row + 1, self.position.column - 1]
                )
                self.legal_moves["kill"].append(back_left_eat)
            if (
                self.board[self.position.row + 1][self.position.column + 1] == "B"
                and self.position.row < 6
                and self.position.column < 7
                and self.board[self.position.row + 2][self.position.column + 2] == "•"
            ):
                back_right_eat = Coordinate(
                    [self.position.row + 1, self.position.column + 1]
                )
                self.legal_moves["kill"].append(back_right_eat)
        else:
            if (
                self.board[self.position.row + 1][self.position.column - 1] == "•"
                and self.position.row < 6
                and self.position.column > 1
            ):
                forward_left = Coordinate(
                    [self.position.row + 1, self.position.column - 1]
                )
                self.legal_moves["move"].append(forward_left)
            if (
                self.board[self.position.row + 1][self.position.column + 1] == "•"
                and self.position.row < 6
                and self.position.column < 7
            ):
                forward_right = Coordinate(
                    [self.position.row + 1, self.position.column + 1]
                )
                self.legal_moves["move"].append(forward_right)
            if (
                self.board[self.position.row + 1][self.position.column - 1] == "W"
                and self.position.row < 6
                and self.position.column > 1
                and self.board[self.position.row + 2][self.position.column - 2] == "•"
            ):
                forward_left_eat = Coordinate(
                    [self.position.row + 1, self.position.column - 1]
                )
                self.legal_moves["kill"].append(forward_left_eat)
            if (
                self.board[self.position.row + 1][self.position.column + 1] == "W"
                and self.position.row < 6
                and self.position.column < 7
                and self.board[self.position.row + 2][self.position.column + 2] == "•"
            ):
                forward_right_eat = Coordinate(
                    [self.position.row + 1, self.position.column + 1]
                )
                self.legal_moves["kill"].append(forward_right_eat)
            if (
                self.board[self.position.row - 1][self.position.column - 1] == "W"
                and self.position.row > 1
                and self.position.column > 1
                and self.board[self.position.row - 2][self.position.column - 2] == "•"
            ):
                back_left_eat = Coordinate(
                    [self.position.row - 1, self.position.column - 1]
                )
                self.legal_moves["kill"].append(back_left_eat)
            if (
                self.board[self.position.row - 1][self.position.column + 1] == "W"
                and self.position.row > 1
                and self.position.column < 7
                and self.board[self.position.row - 2][self.position.column + 2] == "•"
            ):
                back_right_eat = Coordinate(
                    [self.position.row - 1, self.position.column + 1]
                )
                self.legal_moves["kill"].append(back_right_eat)

    def get_moves(self):
        legal_moves_str = [move.coordinate for move in self.legal_moves["move"]]
        legal_kills_str = [move.coordinate for move in self.legal_moves["kill"]]
        print(legal_moves_str)
        print(legal_kills_str)
        all_moves_str = {"move": legal_moves_str, "kill": legal_kills_str}
        return all_moves_str


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
                figure == "W"
                and self.color == "WHITE"
                or figure == "B"
                and self.color == "BLACK"
            ):
                return True
        else:
            return False

    def check_to_cor(self, moves: list) -> bool or str:
        """ Checks if the to coordinate is in the legal moves list of the figure that is chosen """

        if moves["move"].count(self.to_cor.coordinate) == 1:
            return "move"
        elif moves["kill"].count(self.to_cor.coordinate) == 1:
            return "kill"
        else:
            return False

    def validate_move(self) -> bool:
        """ Checks if the given move is legal """

        if self.check_from_cor():
            self.set_figure()
            moves = self.figure.get_moves()
            move_or_kill = self.check_to_cor(moves)
            if move_or_kill:
                return move_or_kill
            else:
                print(f"Illegal move for figure {self.figure.name}")
                return False
        else:
            print("No figure on the first coordinate or you've chozen oponent's figure")
            return False

    def make_move(self):
        """ Changes figure position on bard """

        self.board[self.from_cor.row][self.from_cor.column] = "•"
        self.board[self.to_cor.row][self.to_cor.column] = self.figure.name

    def kill(self):
        """ Kills oponent's checker """

        self.board[self.from_cor.row][self.from_cor.column] = "•"
        self.board[self.to_cor.row][self.to_cor.column] = "•"
        x = self.to_cor.row - self.from_cor.row
        y = self.to_cor.column - self.from_cor.column
        self.board[self.to_cor.row + x][self.to_cor.column + y] = self.figure.name
        self.from_cor = Coordinate([self.to_cor.row + x, self.to_cor.column + y])
        self.set_figure()
        more_kills = self.figure.get_moves()["kill"]
        if len(more_kills) >= 1:
            self.to_cor = Coordinate(more_kills[0])
            self.kill()

    def set_figure(self):
        """ Sets figure wich stands in the from coordinate """

        figure_name = self.get_figure(self.from_cor)
        if figure_name != "•":
            self.figure = Checker(self.color, self.from_cor, self.board)


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

                        Welcome to the game of checkers!!!
                                Instructions:
        1) If you want to exit just type 'exit'
        2) To make a move you need to type in coordinate of the figure that 
           needs to be moved, space and a coordinate of where you want your
           figure to move. For example: 'a2 a3' or 'F2 H3'
        3) If you want to see how many moves were made, type in 'moves'
        4) If you want to read instruction again, type in 'instruction'

        """
        )

    def player_input(self) -> str:
        """ Gets an input from a player """

        if self.status == "WHITE":
            inp = str(input("Move for white!\n"))
        else:
            inp = str(input("Move for black!\n"))

        return inp

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
            inp = self.player_input()
            coordinates = self.process_input(inp)
            if coordinates:  # Coordinates are writen in the right format
                move = Move(
                    coordinates[0], coordinates[1], self.board.board, self.status
                )
                type_of_move = move.validate_move()
                if type_of_move == "move":  # Move can be done
                    move.make_move()
                    self.board.print_board()
                    self.change_status()
                elif type_of_move == "kill":
                    move.kill()
                    self.board.print_board()
                    self.change_status()
            else:
                pass


Gameplay()
