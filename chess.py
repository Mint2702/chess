import sys


class Board:
    def __init__(self):
        self.board_init()
        self.print_board()

    def board_init(self):
        """ Sets start values for board list """

        self.board = [
            "8rnbqkbnr8",
            "7pppppppp7",
            "6••••••••6",
            "5••••••••5",
            "4••••••••4",
            "3••••••••3",
            "2PPPPPPPP2",
            "1RNBQKBNR1",
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
                    print(self.board[i][j], end=" ")
            print()
        print("║ ╚═════════════════╝ ║")
        print("║   A B C D E F G H   ║")
        print("╚═════════════════════╝")


class Coordinate:
    def __init__(self, coordinate: str):
        coordinate = self.validate(coordinate)
        if coordinate:
            self.coordinate = coordinate
            self.row = self.parce_row()
            self.column = self.parce_column()
        else:
            self.coordinate = False

    def validate(self, coordinate: str) -> list or bool:
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

    def parce_row(self) -> int:
        """ Converts row number to the first index for Board obj """

        row = 8 - int(self.coordinate[1])
        return row

    def parce_column(self) -> int:
        """ Converts column letter to the second index for Board obj """

        column = ord(self.coordinate[0]) - 96
        return column


class Move:
    def __init__(self, from_cor: Coordinate, to_cor: Coordinate):
        self.from_cor = from_cor
        self.to_cor = to_cor

    def check_from_cor(self) -> str or bool:
        pass


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
            print("Please check your input and try again")
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
                    self.change_status()  # Надо будет переместить в другое место
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
            if coordinates:
                for coordinate in coordinates:
                    print(coordinate.column)
            else:
                print("AIAIAI")


Gameplay()
