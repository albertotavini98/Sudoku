import pygame
import data_structures

class GraphicalInterface:
    def __init__(self):
        self.sudokuTable = data_structures.SudokuTable()
        self.difficulty = data_structures.Difficulty.LOW

       

    def runGame(self):
        pygame.init()

        # Set up the window
        window_size = (800, 800)
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Sudoku")

        # Set up colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)
        cell_size = 70
        board_size = cell_size * 9
        submatrix_size = cell_size * 3

        sudoku = self.sudokuTable
        sudoku.pickInitialization('initializations')
        #sudoku.randomInitialization(self.difficulty)

        running = True
        while running:
            #here we deal with mouse clicks and keyboard presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    # Calculate the clicked cell indices
                    selected_row = mouse_pos[1] // cell_size
                    selected_col = mouse_pos[0] // cell_size
                    # Modify the clicked cell value
                    
                elif event.type == pygame.KEYDOWN:
                    try:
                        if event.key == pygame.K_1:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(1))
                        elif event.key == pygame.K_2:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(2))
                        elif event.key == pygame.K_3:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(3))
                        elif event.key == pygame.K_4:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(4))
                        elif event.key == pygame.K_5:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(5))
                        elif event.key == pygame.K_6:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(6))
                        elif event.key == pygame.K_7:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(7))
                        elif event.key == pygame.K_8:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(8))
                        elif event.key == pygame.K_9:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(str(9))
                        elif event.key == pygame.K_BACKSPACE:
                            sudoku.getMatrix()[selected_row][selected_col].assignVal(' ')
                    except:
                        print("Exception! no values can be inserted there")

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if 650 <= mouse_pos[0] <= 750 and 720 <= mouse_pos[1] <= 760:
                        print("you demanded a reset")
                        # Reset button clicked
                        sudoku.resetTable()
                    elif 650 <= mouse_pos[0] <= 750 and 670 <= mouse_pos[1] <= 710:
                        print("you demanded a resolution")
                        # Solve button clicked
                        n = 0
                        while n <50:
                            sudoku.solvingIteration()
                            n +=1

                    # Clear the window
                window.fill(WHITE)
            #we draw the game board, using more thick lines to delimit the 3x3 submatrices
            for x in range(0, board_size + 1, cell_size):
                line_color = GRAY if x % submatrix_size == 0 else BLACK
                line_thickness = 4 if x % submatrix_size == 0 else 1

                pygame.draw.line(window, line_color, (x, 0), (x, board_size), line_thickness)
                pygame.draw.line(window, line_color, (0, x), (board_size, x), line_thickness)

            #we fill the game board
            for i in range(9):
                for j in range(9):
                    #for all the boxes we print the value if it has been given 
                    if sudoku.getMatrix()[i][j].getVal() != ' ':
                        font = pygame.font.Font(None, 36)
                        text = font.render(sudoku.getMatrix()[i][j].getVal(), True, BLACK)
                        text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
                        window.blit(text, text_rect)
                    #otherwise we print the list of possible values for it
                    elif len(sudoku.getMatrix()[i][j].getPossibles() ) < 10:
                        for k, possible in enumerate(sudoku.getMatrix()[i][j].getPossibles()):
                            font = pygame.font.Font(None, 18)
                            text = font.render(possible, True, BLACK)
                            #we have to offset because we have to write nine small numbers instead of one
                            offset_x = cell_size//4 + cell_size* ((k+3)%3) //4
                            offset_y = cell_size* ((k+3)//3) //4
                            
                            text_rect = text.get_rect(center=(j * cell_size  + offset_x, i * cell_size +offset_y ))
                            
                            window.blit(text, text_rect)

            # Draw reset button
            pygame.draw.rect(window, (200, 200, 200), (650, 720, 100, 40))
            font = pygame.font.Font(None, 28)
            text = font.render("Reset", True, BLACK)
            text_rect = text.get_rect(center=(700, 740))
            window.blit(text, text_rect)

            # Draw solve button
            pygame.draw.rect(window, (200, 200, 200), (650, 670, 100, 40))
            text = font.render("Solve", True, BLACK)
            text_rect = text.get_rect(center=(700, 690))
            window.blit(text, text_rect)

                    



            # Update the display
            pygame.display.flip()
