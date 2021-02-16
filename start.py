import os
from array import *
def Print_Board():
    print("╔═════════════════════╗")
    print("║   A B C D E F G H   ║")
    print("║ ╔═════════════════╗ ║")
    for i in range(0, 8):
        for j in range(0, 10):
            if j == 0 or j == 9:
                print('║' + board[i][j] + '║', end = ' ')
            else:
                print(board[i][j], end = ' ')
        print()
    print("║ ╚═════════════════╝ ║")
    print("║   A B C D E F G H   ║")
    print("╚═════════════════════╝")

def Input_Validation():
    if len(command) != 5:
        print("Command length is not 5 characters")
        return False
    if command[2] != ' ':
        print("Put a space between the coordinates of the shapes")
        return False
    if ord(command[0]) < 65 or ord(command[0]) > 72 or ord(command[3]) < 65 or ord(command[3]) > 72: 
        print("These symbols are not on the board")
        return False
    if int(command[1]) < 1 or int(command[1]) > 8 or int(command[4]) < 1 or int(command[4]) > 8:
        print("these values are not on the board")
        return False
    return True

def Move_Validation():
    figure = board[8 - int(command[1])][ord(command[0]) - 64]
    if figure == "•":
        print("There is no figure!")
        return False
    if countMove % 2 == 0:
        if ord(figure) > 96:
            print("This is not your figure!")
            return False
    else:
        if ord(figure) < 91:
            print("This is not your figure!")
            return False
    return CheckFigurePos(figure)

def Check_Cells_Rook(distanceX, distanceY, thisPosX, thisPosY, posX):
    if distanceX > 0 and distanceY > 0:
        y = thisPosY - 1
        for x in range(thisPosX + 1, posX):
            if board[y][x] != '•':
                print("The figure is getting in the way!")
                return False
            y -= 1
    elif distanceX < 0 and distanceY > 0:
        y = thisPosY - 1
        for x in range(thisPosX - 1, posX, -1):
            if board[y][x] != '•':
                print("The figure is getting in the way!")
                return False
            y -= 1
    elif distanceX < 0 and distanceY < 0:
        y = thisPosY + 1
        for x in range(thisPosX - 1, posX, -1):
            if board[y][x] != '•':
                print("The figure is getting in the way!")
                return False
            y += 1
    else:
        y = thisPosY + 1
        for i in range(thisPosX + 1, posX):
            if board[y][x] != '•':
                print("The figure is getting in the way!")
                return False
            y += 1
    return True

def Check_Cells_Elefant(distanceX, distanceY, thisPosX, thisPosY, posX, posY):
    if distanceX > 0:
        for i in range(thisPosX + 1, posX):
            if board[posY][i] != '•':
                print("The figure is getting in the way!!")
                return False
    elif distanceX < 0:
        for i in range(thisPosX - 1, posX, -1):
            if board[posY][i] != '•':
                print("The figure is getting in the way!")
                return False
    elif distanceY > 0:
        for i in range(thisPosY - 1, posY, -1):
            if board[i][posX] != '•':
                print("The figure is getting in the way!")
                return False
    else:
        for i in range(thisPosY + 1, posY):
            if board[i][posX] != '•':
                print("The figure is getting in the way!")
                return False
    return True


def Check_Figure_Pos(figure):
    thisPosY = 8 - int(command[1])
    thisPosX = ord(command[0]) - 64
    posY = 8 - int(command[4])
    posX = ord(command[3]) - 64
    distanceX = ord(command[3]) - ord(command[0])
    distanceY = int(command[4]) - int(command[1])
    if figure == 'P':
        if command[0] != command[3]:
            if distanceY != 1 or abs(distanceX) != 1:
                print("A pawn doesn't go that far!")
                return False
            if ord(board[posY][posX]) < 97 or ord(board[posY][posX]) > 122:
                print("There is no enemy figure here!")
                return False
        elif int(command[1]) == 2 and distanceY == 2:
            if board[posY][posX] != '•' or board[posY + 1][posX] != '•':
                print("Another figure hinders in the way!")
                return False
        elif distanceY != 1:
            print("A pawn doesn't go that far!")
            return False
        elif board[posY][posX] != '•':
            print("This position is taken!")
            return False
    elif figure == 'p':
        if command[0] != command[3]:
            if distanceY != -1 or abs(distanceX) != 1:
                print("A pawn doesn't go that far!")
                return False
            if ord(board[posY][posX]) < 65 or ord(board[posY][posX]) > 90:
                print("There is no enemy here!")
                return False
        elif int(command[1]) == 7 and distanceY == -2:
            if board[posY][posX] != '•' or board[posY - 1][posX] != '•':
                print("Another figure hinders in the way!")
                return False
        elif distanceY != -1:
            print("A pawn doesn't go that far!")
            return False
        elif board[posY][posX] != '•':
            print("This position is taken!")
            return False
    
    elif figure == 'R':
        if abs(distanceX) > 0 and abs(distanceY) > 0:
            print("The rook moves only in a straight line!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("You haven't changed the position of the figure!")
        if not CheckCellsElefant(distanceX, distanceY, thisPosX, thisPosY, posX, posY):
                return False
        if ord(board[posY][posX]) > 64 and ord(board[posY][posX]) < 91:
            print("This position is taken!")
            return False
   
    elif figure == 'r':
        if abs(distanceX) > 0 and abs(distanceY) > 0:
            print("The rook moves only in a straight line!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
        if not CheckCellsElefant(distanceX, distanceY, thisPosX, thisPosY, posX, posY):
            return False
        if ord(board[posY][posX]) > 96 and ord(board[posY][posX]) < 123:
            print("This position is taken!")
            return False
        
    elif figure == 'N':
        if abs(distanceX) > 2 or abs(distanceY) > 2:
            print("The horse doesn't go that far!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
            return False
        if (abs(distanceX) != 1 or abs(distanceY) != 2) and (abs(distanceX) != 2 or abs(distanceY) != 1):
            print("The horse moves with the letter 'G'")
            return False
        if ord(board[posY][posX]) > 64 and ord(board[posY][posX]) < 91:
            print("This position is taken")
            return False
    
    elif figure == 'n':
        if abs(distanceX) > 2 or abs(distanceY) > 2:
            print("The horse doesn't go that far!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
            return False
        if (abs(distanceX) != 1 or abs(distanceY) != 2) and (abs(distanceX) != 2 or abs(distanceY) != 1):
            print("The horse moves with the letter 'G'")
            return False
        if ord(board[posY][posX]) > 96 and ord(board[posY][posX]) < 123:
            print("This position is taken!")
            return False
    
    elif figure == 'B':
        if abs(distanceX) != abs(distanceY):
            print("the elephant walks only obliquely!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
        if not CheckCellsRook(distanceX, distanceY, thisPosX, thisPosY, posX):
            return False
        if ord(board[posY][posX]) > 64 and ord(board[posY][posX]) < 91:
            print("This posisition is taken!")
            return False
    
    elif figure == 'b':
        if abs(distanceX) != abs(distanceY):
            print("the elephant walks only obliquely!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
        if not CheckCellsRook(distanceX, distanceY, thisPosX, thisPosY, posX):
            return False
        if ord(board[posY][posX]) > 96 and ord(board[posY][posX]) < 123:
            print("This position is taken!")
            return False
    
    elif figure == 'Q':
        if abs(distanceX) != abs(distanceY) and abs(distanceX) > 0 and abs(distanceY) > 0:
            print("The Queen doesn't go like that!")
            return False
        if abs(distanceX) == abs(distanceY):
            if not CheckCellsRook(distanceX, distanceY, thisPosX, thisPosY, posX):
                return False
        else:
            if not CheckCellsElefant(distanceX, distanceY, thisPosX, thisPosY, posX, posY):
                return False
        if ord(board[posY][posX]) > 64 and ord(board[posY][posX]) < 91:
            print("This position is taken!")
            return False
    
    elif figure == 'q':
        if abs(distanceX) != abs(distanceY) and abs(distanceX) > 0 and abs(distanceY) > 0:
            print("The Queen doesn't go like that!")
            return False
        if abs(distanceX) == abs(distanceY):
            if not CheckCellsRook(distanceX, distanceY, thisPosX, thisPosY, posX):
                return False
        else:
            if not CheckCellsElefant(distanceX, distanceY, thisPosX, thisPosY, posX, posY):
                return False
        if ord(board[posY][posX]) > 96 and ord(board[posY][posX]) < 123:
            print("This position is taken!")
            return False
    
    elif figure == 'K':
        if abs(distanceX) > 1 or abs(distanceY) > 1:
            print("The king moves only 1 square!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
            return False
        if ord(board[posY][posX]) > 64 and ord(board[posY][posX]) < 91:
            print("This position is taken!")
            return False
   
    elif figure == 'k':
        if abs(distanceX) > 1 or abs(distanceY) > 1:
            print("The king moves only 1 square!")
            return False
        if distanceX == 0 and distanceY == 0:
            print("The position of the figure has not changed!")
            return False
        if ord(board[posY][posX]) > 96 and ord(board[posY][posX]) < 123:
            print("This position is taken!")
            return False
    return True

def MoveFigure():
    posY1 = 8 - int(command[1])
    posX1 = ord(command[0]) - 64
    posY2 = 8 - int(command[4])
    posX2 = ord(command[3]) - 64
    figure = board[posY1][posX1]
    newStr = ""
    for i in range(0, 10):
        if i != posX1:
            newStr += board[posY1][i]
        else:
            newStr += '•'
    board[posY1] = newStr 
    newStr = ""
    for i in range(0, 10):
        if i != posX2:
            newStr += board[posY2][i]
        else:
            newStr += figure
    board[posY2] = newStr

def CheckEndGame():
    blackKing = False
    whiteKing = False
    for i in range(0, 8):
        if board[i].find('K') != -1:
            whiteKing = True
        if board[i].find('k') != -1:
            blackKing = True
    if (not blackKing):
        print("White won!")
    if (not whiteKing):
        print("Black won")
    return blackKing & whiteKing 

while(True):
    print("""   Menu
1) Start play
2) Exit""")
    input_ = int(input("Enter menu number: "))
    if input_ == 1:
        board = []
        board.append("8rnbqkbnr8")
        board.append("7pppppppp7")
        board.append("6••••••••6")
        board.append("5••••••••5")
        board.append("4••••••••4")
        board.append("3••••••••3")
        board.append("2PPPPPPPP2")
        board.append("1RNBQKBNR1")
        countMove = 0
        quite = False
        while(not quite):
            os.system("cls")
            print("Write quit to exit to menu \ n")
            print("Moves done: ", countMove)
            Print_Board()
            if countMove % 2 == 0:
                print("Move for white!")
            else:
                print("Move for black!")
            command = input("->> ")
            if command == "quit":
                break
            while (not (Input_Validation() and Move_Validation())):
                command = input("->> ")
                if command == "quit":
                    quite = True
                    break
            if (not quite):
                MoveFigure()
                if (not CheckEndGame()):
                    print("Game end.")
                    break
                countMove+=1
    elif input_ == 2:
        print("Thank you for playing!")
        break
    else:
        print("This menu item is missing!")
    os.system("pause")