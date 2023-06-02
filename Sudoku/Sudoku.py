import data_structures

matrix = data_structures.SudokuTable()
matrix.printTable()
while True:
    print("Enter a set of coordinates and a value in the format 'x-y-val', or 'R' to reset the table")
    user_input = input()
    if matrix.checkInsertString(user_input):
        matrix.printTable()
    elif user_input == 'r':
        matrix.resetTable()
        matrix.printTable()
    elif user_input == 'c':
        if matrix.checkCoherence():
            print("everything is fine")
        else:
            print("you got it wrong, you asshole")
    else:
        print("invalid input format")