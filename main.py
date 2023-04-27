from sudoku_connections import SudokuConnections
import random
from tkinter import *
import sys

sys.setrecursionlimit(20000)

class SudokuBoard : 
    def __init__(self, size = 9) : 
        if size != 9 and size != 16:
            raise ValueError("Size can only be 9 or 16")

        self.size = size
        self.board = self.getDefaultBoard()
        
        self.sudokuGraph = SudokuConnections(self.size)
        self.mappedGrid = self.__getMappedMatrix() # Maps all the ids to the position in the matrix

    def __getMappedMatrix(self) : 
        matrix = [[0 for cols in range(self.size)]  for rows in range(self.size)]

        count = 1
        for rows in range(self.size) : 
            for cols in range(self.size):
                matrix[rows][cols] = count
                count+=1
        return matrix

    def getDefaultBoard(self) : 

        board = [[0 for cols in range(self.size)]  for rows in range(self.size)]
        return board

    def printBoard(self) : 
        
        if self.size == 16 :
            symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]
            # print using tkinter
        
        elif self.size == 9 :
            print("    1 2 3     4 5 6     7 8 9")
            for i in range(len(self.board)) : 
                if i%3 == 0  :#and i != 0:
                    print("  - - - - - - - - - - - - - - ")

                for j in range(len(self.board[i])) : 
                    if j %3 == 0 :#and j != 0 : 
                        print(" |  ", end = "")
                    if j == 8 :
                        print(self.board[i][j]," | ", i+1)
                    else : 
                        print(f"{ self.board[i][j] } ", end="")
            print("  - - - - - - - - - - - - - - ")

    def is_Blank(self) : 
        
        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) : 
                if self.board[row][col] == 0 : 
                    return (row, col)
        return None

    def graphColoringInitializeColor(self):
        """
        fill the already given colors
        """
        color = [0] * (self.sudokuGraph.graph.totalV+1)
        given = [] # list of all the ids whos value is already given. Thus cannot be changed
        for row in range(len(self.board)) : 
            for col in range(len(self.board[row])) : 
                if self.board[row][col] != 0 : 
                    #first get the idx of the position
                    idx = self.mappedGrid[row][col]
                    #update the color
                    color[idx] = self.board[row][col] # this is the main imp part
                    given.append(idx)
        return color, given

    def solveGraphColoring(self, m =9) : 
        
        color, given = self.graphColoringInitializeColor()
        if self.__graphColorUtility(m =m, color=color, v =1, given=given) is None :
            print(":(")
            return False
        count = 1
        for row in range(self.size) : 
            for col in range(self.size) :
                self.board[row][col] = color[count]
                count += 1
        return color
    
    def __graphColorUtility(self, m, color, v, given) :
        
        if v == self.sudokuGraph.graph.totalV+1  : 
            return True
        safecolors = []
        for c in range(1, m+1):
            if self.__isSafe2Color(v, color, c, given) == True :
                safecolors.append(c)
        
        random.shuffle(safecolors)

        for c in safecolors :
            color[v] = c
            if self.__graphColorUtility(m, color, v+1, given) : 
                return True
            if v not in given : 
                color[v] = 0

    def __isSafe2Color(self, v, color, c, given) : 
        
        if v in given and color[v] == c: 
            return True
        elif v in given : 
            return False

        for i in range(1, self.sudokuGraph.graph.totalV+1) :
            if color[i] == c and self.sudokuGraph.graph.isNeighbour(v, i) :
                return False
        return True
    
    def getSudokuProblem(difficulty = "easy", size = 9):
        s = SudokuBoard(size)
        s.solveGraphColoring(size)
        fraction = 0.2
        if difficulty == "easy" :
            fraction = 0.2
        elif difficulty == "medium" :
            fraction = 0.45
        elif difficulty == "hard" :
            fraction = 0.9
        for row in range(len(s.board)) :
            for col in range(len(s.board[row])) : 
                if random.random() < fraction : 
                    s.board[row][col] = 0
        return s.board
    
    def setBoard(self, board):
        self.board = board

    def checkBoard(self) : 
        """
        check if the problem is valid or not
        """
        for row in range(len(self.board)) : 
            for col in range(len(self.board[row])) : 
                if self.board[row][col] == 0 : 
                    continue
                if self.__checkRow(row, col) == False or self.__checkCol(row, col) == False or self.__checkSubGrid(row, col) == False :
                    return False
            return True
    
    def __checkRow(self, row, col) : 
        for i in range(len(self.board[row])) : 
            if i == col : 
                continue
            if self.board[row][i] == self.board[row][col] : 
                return False
        return True
    
    def __checkCol(self, row, col) :
        for i in range(len(self.board)) : 
            if i == row : 
                continue
            if self.board[i][col] == self.board[row][col] : 
                return False
        return True
    
    def __checkSubGrid(self, row, col) :
        if self.size == 9 : 
            if row < 3 : 
                row = 0
            elif row < 6 : 
                row = 3
            else : 
                row = 6
            if col < 3 : 
                col = 0
            elif col < 6 : 
                col = 3
            else : 
                col = 6
            for i in range(row, row+3) : 
                for j in range(col, col+3) : 
                    if i == row and j == col : 
                        continue
                    if self.board[i][j] == self.board[row][col] : 
                        return False
            return True
        elif self.size == 16 : 
            if row < 4 : 
                row = 0
            elif row < 8 : 
                row = 4
            elif row < 12 : 
                row = 8
            else : 
                row = 12
            if col < 4 : 
                col = 0
            elif col < 8 : 
                col = 4
            elif col < 12 : 
                col = 8
            else : 
                col = 12
            for i in range(row, row+4) : 
                for j in range(col, col+4) : 
                    if i == row and j == col : 
                        continue
                    if self.board[i][j] == self.board[row][col] : 
                        return False
            return True


b = []

def main() :

    window = Tk()
    window.title("Sudoku Solver")
    #resizable window with a fixed aspect ratio of 1.5
    window.resizable(False, False)
    window.geometry("1366x768")

    
    # Add a label for the title
    title = Label(window, text = "Sudoku Solver by Vignaraj, 211IT080", font = ("Arial", 20), bg = "white")
    title.pack(side = TOP, pady = 10)


    window.configure(bg = "white")

    #create a frame for the sudoku board
    boardFrame = Frame(window, bg = "white")
    boardFrame.pack(side = TOP, pady = 10)

    def clear_frame():
        for widgets in boardFrame.winfo_children():
            widgets.destroy()

    #create a frame for the buttons
    buttonFrame = Frame(window, bg = "white")
    buttonFrame.pack(side = TOP, pady = 10)

    #create a frame for the difficulty buttons
    difficultyFrame = Frame(window, bg = "white")
    difficultyFrame.pack(side = TOP, pady = 10)

    #create a frame for the size buttons
    sizeFrame = Frame(window, bg = "white")
    sizeFrame.pack(side = TOP, pady = 10)

    #create a frame for the solution
    solutionFrame = Frame(window, bg = "white")
    solutionFrame.pack(side = TOP, pady = 10)

    # Add a label for the difficulty
    difficultyLabel = Label(difficultyFrame, text = "Difficulty", font = ("Arial", 15), bg = "white")
    difficultyLabel.pack(side = LEFT, padx = 10)

    # Choice for difficulty
    difficulty = StringVar()
    difficulty.set("easy")
    easy = Radiobutton(difficultyFrame, text = "Easy", variable = difficulty, value = "easy", bg = "white")
    easy.pack(side = LEFT, padx = 10)
    medium = Radiobutton(difficultyFrame, text = "Medium", variable = difficulty, value = "medium", bg = "white")
    medium.pack(side = LEFT, padx = 10)
    hard = Radiobutton(difficultyFrame, text = "Hard", variable = difficulty, value = "hard", bg = "white")
    hard.pack(side = LEFT, padx = 10)

    # Add a label for the size
    sizeLabel = Label(sizeFrame, text = "Size", font = ("Arial", 15), bg = "white")
    sizeLabel.pack(side = LEFT, padx = 10)

    _difficulty = 0
    _size = 0
    # detect clicks and update the size and difficulty
    def updateSizeDifficulty():
        _difficulty = difficulty.get()
        _size = size.get()
        clear_frame()

    # Choice for size
    size = IntVar()
    size.set(9)
    nine = Radiobutton(sizeFrame, text = "9x9", variable = size, value = 9, bg = "white", command = updateSizeDifficulty)
    nine.pack(side = LEFT, padx = 10)
    sixteen = Radiobutton(sizeFrame, text = "16x16", variable = size, value = 16, bg = "white", command = updateSizeDifficulty)
    sixteen.pack(side = LEFT, padx = 10)

    # get size and difficulty
    _difficulty = difficulty.get()
    _size = size.get()


    # Add a button to generate the problem
    generateButton = Button(buttonFrame, text = "Generate", font = ("Arial", 15), bg = "white", command = lambda : generateProblem(boardFrame, _difficulty, _size))
    generateButton.pack(side = LEFT, padx = 10)    

    def generateProblem(boardFrame, _difficulty, _size):
        _size = size.get()
        _difficulty = difficulty.get()
        s = SudokuBoard(_size)
        s.setBoard(SudokuBoard.getSudokuProblem(_difficulty, _size))
        b = s.board
        clear_frame()

        for i in range(_size):
            for j in range(_size):
                if b[i][j] == 0:
                    entry = Entry(boardFrame, width = 2, font = ("Arial", 20), justify = "center")
                    entry.grid(row = i, column = j)
                else:
                    entry = Entry(boardFrame, width = 2, font = ("Arial", 20), justify = "center")
                    entry.grid(row = i, column = j)
                    entry.insert(0, b[i][j])
                    entry.config(state = "disabled")
        
        # Add a button to solve the problem if there is no solve buttin present
        if len(buttonFrame.winfo_children()) == 1:
            solveButton = Button(buttonFrame, text = "Solve", font = ("Arial", 15), bg = "white", command = lambda : solveProblem(boardFrame, solutionFrame, _size))
            solveButton.pack(side = LEFT, padx = 10)

    def solveProblem(boardFrame, solutionFrame, _size):
        #create a board object
        s = SudokuBoard(_size)
        b = []
        for i in range(_size):
            row = []
            for j in range(_size):
                entry = boardFrame.grid_slaves(row = i, column = j)[0]
                if entry.get() == "":
                    row.append(0)
                else:
                    row.append(int(entry.get()))
            b.append(row)
        s.setBoard(b)
        s.solveGraphColoring(_size)
        b = s.board
        clear_frame()

        for i in range(_size):
            for j in range(_size):
                entry = Entry(boardFrame, width = 2, font = ("Arial", 20), justify = "center")
                entry.grid(row = i, column = j)
                entry.insert(0, b[i][j])
                entry.config(state = "disabled")

    window.mainloop()

if __name__ == "__main__" : 
    main()
