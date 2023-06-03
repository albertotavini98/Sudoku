
from tkinter import SE
import copy

class SudokuUnit:
    def __init__(self):
        self.val = ' '
        self.possibles = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def getVal(self):
        return self.val

    def getPossibles(self):
        return self.possibles

    def getUnitRepresentation(self):
        if self.val != ' ':
            digits = [self.val]*9
        elif len(self.possibles) == 9:
            digits = [' ']*9
        else:
            digits = self.possibles

        box = ""
        for i in range(3):
                row = "| {} {} {} |\n".format(*(digits[i * 3: i * 3 + 3] + [' '] * (3 - len(digits[i * 3: i * 3 + 3]))))
                box += row
        return box

    def assignVal(self, val):
        self.val = str(val) if val != 0 else ' '
    





class SudokuTable:
    def __init__(self):
        self.original_matrix = [[SudokuUnit() for i in range(9)] for j in range(9)]
        self.matrix = copy.deepcopy( self.original_matrix)
        self.symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']

    def getMatrix(self):
        return self.matrix

    def resetTable(self):
        self.matrix = copy.deepcopy( self.original_matrix)

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
        if self.original_matrix.getVal() == ' ':
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
    def divideIn3by3(self):
        submatrices_as_lists = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                submatrix = [num for row in self.matrix[i:i+3] for num in row[j:j+3]]
                submatrices_as_lists.append(submatrix)

        return submatrices_as_lists


    #this method checks if the rows, columns and submatrices of the table respect the sudoku property and returns True if it does
    def checkCoherence(self):
        for row in self.matrix:
            if not self.checkDigitsInUnits(row):
                return False

        for column in zip(*self.matrix):
            if not self.checkDigitsInUnits(column):
                return False

        submatrices_as_lists = self.divideIn3by3()

        for item in submatrices_as_lists:
            if not self.checkDigitsInUnits(item):
                return False

        return True