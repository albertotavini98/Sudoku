class SudokuUnit:
    def __init__(self):
        self.val = ' '
        self.possibles = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def getVal(self):
        return self.val


    #this is for assignment from integer, if we clean it we restore the possible values
    def assignVal(self, val):
        self.val = val
        if self.val == ' ':
           self.possibles = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        else:
            self.possibles = []

    def getPossibles(self):
        return self.possibles

    def removeFromPossibles(self, value):
        if value in self.possibles:
            self.possibles.remove(value)
            return True
        else:
            return False

    def addToPossibles(self, value):
        if value not in self.possibles:
            self.possibiles.append(value)
            return True
        else:
            return False

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
