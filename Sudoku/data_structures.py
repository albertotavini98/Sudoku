
from tkinter import SE


class SudokuTable:
    def __init__(self):
        self.matrix = [['_']*9 for _ in range(9)]

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

    def insertValue(self, x, y, val):
         self.matrix[x][y] = str(val)


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