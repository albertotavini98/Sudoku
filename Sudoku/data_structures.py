
from tkinter import SE


class SudokuTable:
    def __init__(self):
        self.matrix = [['_']*9 for _ in range(9)]
        self.symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '_']

    

    def resetTable(self):
        self.matrix = [['_']*9 for _ in range(9)] 

    #this function prints the 
    def printTable(self):

        for j, row in enumerate(self.matrix):
            if j %3 == 0 and j!= 0:
                print("")
            
            for i, value in enumerate(row):
                item = '['+value+']'
                if i%3 == 0 and i!= 0:
                    print("  "+item, end= "")
                else:
                    print(item, end ="" )

            print("")


    #we insert a value if bigger than zero else we empty that cell
    def insertValue(self, x, y, val):
         self.matrix[x][y] = str(val) if val != 0 else '_'


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
    def checkDigits(self, chars):
        symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for c in chars:
            if c != '_':
                if c not in symbols:
                    return False
                else:
                    symbols.remove(c)

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
            if not self.checkDigits(row):
                return False

        for column in zip(*self.matrix):
            if not self.checkDigits(column):
                return False

        submatrices_as_lists = self.divideIn3by3()

        for item in submatrices_as_lists:
            if not self.checkDigits(item):
                return False

        return True