
from tkinter import SE
import copy
import random
from enum import Enum
from sudokublock import SudokuUnit


class Difficulty(Enum):
    LOW = 30
    MEDIUM = 25
    HIGH = 20





class SudokuTable:
    def __init__(self):
        self.originalMatrix = [[SudokuUnit() for i in range(9)] for j in range(9)]
        self.checkMatrix = None
        self.matrix = None
        self.savedMatrix = None
        self.symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
        self

    def getMatrix(self):
        return self.matrix

    #initializations are saved as .txt. files 
    #and contenti is taken from the compact output format generated from https://qqwing.com/generate.html
    def pickInitialization(self, folder):
        import os
        files = os.listdir(folder)
        txt_files = [file for file in files if file.endswith(".txt")]
        chosen_file = random.choice(txt_files)
        file_path = os.path.join(folder, chosen_file)
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Content of file '{chosen_file}':")
            rows = content.split('\n')
            for i, row in enumerate(rows):
                for j ,char in enumerate(row):
                    if char != '.':
                        self.originalMatrix[i][j].assignVal(char)

        self.checkMatrix = copy.deepcopy(self.originalMatrix)
        self.matrix = copy.deepcopy(self.originalMatrix)
        self.savedMatrix = copy.deepcopy(self.originalMatrix)



    #obviously if you use this there is high probability the sudoku cannot be solved 
    def randomInitialization(self, difficulty):
        counter = difficulty.value
        while counter > 0:
            #we generate an insertion
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            val = random.randint(1,9)
            #if the box is empty
            if self.originalMatrix[x][y].getVal() == ' ':
                #we copy the matrix
                self.checkMatrix = copy.deepcopy(self.originalMatrix)
                #then insert and check consistence with sudoku property, and if correct we decrease the number of entries to make, otherwise we copy again the matrix
                self.originalMatrix[x][y].assignVal(str(val))
                if not self.checkCoherence(True):
                     self.originalMatrix = copy.deepcopy(self.checkMatrix)
                else:
                    counter -= 1

        
        self.checkMatrix = copy.deepcopy(self.originalMatrix)
        self.matrix = copy.deepcopy(self.originalMatrix)
        self.savedMatrix = copy.deepcopy(self.originalMatrix)


    def resetTable(self):
        self.matrix = copy.deepcopy( self.originalMatrix)

    #this uses the box representation of all the 
    def printRow(self, boxes):
        boxes_by_lines =[]
        
        for i in range(len(boxes)):
            boxes_by_lines.append(boxes[i].split('\n'))
     
        row = ""
        for i in range(3):
            row_line = ""
            for j, box_line in enumerate(boxes_by_lines):
                row_line += box_line[i]
                if (j+1)%3== 0:
                        row_line += " "
            row_line += "\n"
            row += row_line
        print(row)
            


    #this function prints all the SudokuUnits inside a  
    def printTable(self):

        for j, row in enumerate(self.matrix):
            if j %3 == 0 and j!= 0:
                print("")
            boxes = []
            for i, unit in enumerate(row):
              
                boxes.append(unit.getUnitRepresentation())
            self.printRow(boxes)

            print("")


    #we insert a value if possible (we check it was an empty cell in the original matrix ) and return boolean
    def insertValue(self, x, y, val):
        if self.originalMatrix.getVal() == ' ':
            self.matrix[x][y].assignVal(val)
            return True
        else:
            return False


    #this method check if a string is in the format 'x-y-val' and if yes modifies the table and returns True, else it returns False
    def checkInsertString(self, string):
        if len(string) != 5:
            return False
        if string[1] != '-' or string[3] != '-':
            return False
        if not string[0].isdigit() or not string[2].isdigit() or not string[4].isdigit():
            return False

        x, y, val = int(string[0]) , int(string[2]) , int(string[4])
        self.insertValue(x, y, val)

        return True

    #this method checks if a list representing a row, column or submatrix has duplicate digits and returns False in that case
    def checkDigitsInUnits(self, units):
        symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for unit in units:
            if unit.val != ' ':
                if unit.val not in symbols:
                    return False
                else:
                    symbols.remove(unit.val)

        return True

    #this method divides the matrix in 3x3 submatrices and returns them as a list of lists, so we can use the checkDigits method on them
    def divideIn3by3(self, original = False):
        #check which matrix we need to use
        matrix = self.originalMatrix if original else self.matrix
        submatrices_as_lists = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                submatrix = [num for row in matrix[i:i+3] for num in row[j:j+3]]
                submatrices_as_lists.append(submatrix)

        return submatrices_as_lists


    #this method checks if the rows, columns and submatrices of the table respect the sudoku property and returns True if it does
    #the second parameter needs to be set to true if we want to check on the original matrix during initialization
    def checkCoherence(self, original = False):
        #check which matrix we need to use
        matrix = self.originalMatrix if original else self.matrix

        for row in matrix:
            if not self.checkDigitsInUnits(row):
                return False

        for column in zip(*matrix):
            if not self.checkDigitsInUnits(column):
                return False

        submatrices_as_lists = self.divideIn3by3()

        for item in submatrices_as_lists:
            if not self.checkDigitsInUnits(item):
                return False

        return True

    #this function does one check for all the rows, one for all the columns and one for all the submatrices 
    #and reduces the possibles list by confronting with available values.
    #if one list becomes equal to one, it sets the value of the cell to that value
    def solvingIteration(self):

        #we use a helper function to cross compare
        def compareBoxes(boxes):
            values = [box.getVal() for box in boxes if box.getVal() != ' ']
            for box in boxes:
                for val in values:
                    box.removeFromPossibles(val)
        #and one helper function to assign a value
        def confirmValues(boxes):
            for box in boxes:
                if len(box.getPossibles()) == 1 and box.getVal() == ' ':
                    box.assignVal(box.getPossibles()[0])

        submatrices_as_lists = self.divideIn3by3()
        for item in submatrices_as_lists:
            compareBoxes(item)

        for row in self.matrix:
            compareBoxes(row)
            confirmValues(row)

        for column in zip(*self.matrix):
            compareBoxes(column)
            confirmValues(column)
    
    #a method to see if the game has been solved
    def checkSolved(self):
        for row in self.matrix:
            for box in row:
                if box.getVal() == ' ':
                    return False

        return True

    #a method to solve the entire game
    def solve(self):
        cont = True
        n = 0
        while cont:
            self.solvingIteration()
            if (n% 20 == 0 and self.checkSolved()) or n == 50:
                cont = False
            n +=1

    def saveState(self):
        self.savedMatrix = copy.deepcopy(self.matrix)

    def revertState(self):
        self.matrix = copy.deepcopy(self.savedMatrix)
        self.checkMatrix = copy.deepcopy(self.savedMatrix)





        

        


            