import pygame
import data_structures
from data_structures import Difficulty

class GraphicalInterface:
    def __init__(self):
        self.sudokuTable = data_structures.SudokuTable()
        self.difficulty = Difficulty.LOW

    
    #a method so that a first window pops up allowing to choose a difficulty for the game
    def initialize_interface(self):
        pygame.init()

        window_width = 400
        window_height = 450
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Sudoku's Difficulty")

        # Create a clock object to control the frame rate
        clock = pygame.time.Clock()

        # Set up the font
        font = pygame.font.Font(None, 36)

        # Set up the boxes
        box_width = 200
        box_height = 50
        box_padding = 20
        box_x = window_width // 2 - box_width // 2
        box_y = 200
        box_low = pygame.Rect(box_x, box_y, box_width, box_height)
        box_medium = pygame.Rect(box_x, box_y + box_height + box_padding, box_width, box_height)
        box_high = pygame.Rect(box_x, box_y + (box_height + box_padding) * 2, box_width, box_height)

        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if box_low.collidepoint(mouse_pos):
                        self.difficulty = Difficulty.LOW
                        running = False
                    elif box_medium.collidepoint(mouse_pos):
                        self.difficulty = Difficulty.MEDIUM
                        running = False
                    elif box_high.collidepoint(mouse_pos):
                        self.difficulty = Difficulty.HIGH
                        running = False

            # Clear the screen
            window.fill((255, 255, 255))

            # Render the text and boxes
            text = font.render("Choose a difficulty:", True, (0, 0, 0))
            text_rect = text.get_rect(center=(window_width // 2, 100))
            window.blit(text, text_rect)

            pygame.draw.rect(window, (0, 0, 0), box_low, 2)
            text_low = font.render("Low", True, (0, 0, 0))
            text_rect_low = text_low.get_rect(center=box_low.center)
            window.blit(text_low, text_rect_low)

            pygame.draw.rect(window, (0, 0, 0), box_medium, 2)
            text_medium = font.render("Medium", True, (0, 0, 0))
            text_rect_medium = text_medium.get_rect(center=box_medium.center)
            window.blit(text_medium, text_rect_medium)

            pygame.draw.rect(window, (0, 0, 0), box_high, 2)
            text_high = font.render("High", True, (0, 0, 0))
            text_rect_high = text_high.get_rect(center=box_high.center)
            window.blit(text_high, text_rect_high)

            # Update the display
            pygame.display.flip()

            # Limit the frame rate to 30 FPS
            clock.tick(30)

        # Quit Pygame
        pygame.quit()


    #a utility method to draw the board of the sudoku game
    def drawGameBoard(self, sudoku, board_size, cell_size, submatrix_size, window, showPossibles):
        BLACK = (0, 0, 0)
        GRAY = (128, 128, 128)
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
                    elif showPossibles and len(sudoku.getMatrix()[i][j].getPossibles() ) < 10:
                        for k, possible in enumerate(sudoku.getMatrix()[i][j].getPossibles()):
                            font = pygame.font.Font(None, 18)
                            text = font.render(possible, True, BLACK)
                            #we have to offset because we have to write nine small numbers instead of one
                            offset_x = cell_size//4 + cell_size* ((k+3)%3) //4
                            offset_y = cell_size* ((k+3)//3) //4
                            
                            text_rect = text.get_rect(center=(j * cell_size  + offset_x, i * cell_size +offset_y ))
                            
                            window.blit(text, text_rect)


        

    def runGame(self):
        pygame.init()

        # Set up the window
        window_size = (1050, 700)
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Sudoku")

        # Set up colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)
        LIGHT_RED = (225, 125, 125)
        LIGHT_BLUE = ( 100, 100, 175)
        LIGHT_GREEN = ( 100, 175, 100)
        LIGHT_GRAY = (200, 200, 200)
        cell_size = 70
        board_size = cell_size * 9
        submatrix_size = cell_size * 3

        sudoku = self.sudokuTable
        sudoku.pickInitialization('initializations')
        touchPossibles = False
        showPossibles = False

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
                        #if we toggle the spacebar we want to modify the list of possibles
                        if event.key == pygame.K_SPACE:
                            touchPossibles = not touchPossibles
                        elif event.key == pygame.K_CAPSLOCK:
                            showPossibles = not showPossibles
                        #so if not toggled we just modify the number in the cell
                        if not touchPossibles:
                            try:
                                if event.key == pygame.K_BACKSPACE:
                                    sudoku.tryMove(selected_row, selected_col,' ')
                                elif event.key == pygame.K_1:
                                    sudoku.tryMove(selected_row, selected_col,str(1))
                                elif event.key == pygame.K_2:
                                     sudoku.tryMove(selected_row, selected_col,str(2))
                                elif event.key == pygame.K_3:
                                     sudoku.tryMove(selected_row, selected_col,str(3))
                                elif event.key == pygame.K_4:
                                     sudoku.tryMove(selected_row, selected_col,str(4))
                                elif event.key == pygame.K_5:
                                     sudoku.tryMove(selected_row, selected_col,str(5))
                                elif event.key == pygame.K_6:
                                     sudoku.tryMove(selected_row, selected_col,str(6))
                                elif event.key == pygame.K_7:
                                     sudoku.tryMove(selected_row, selected_col,str(7))
                                elif event.key == pygame.K_8:
                                     sudoku.tryMove(selected_row, selected_col,str(8))
                                elif event.key == pygame.K_9:
                                     sudoku.tryMove(selected_row, selected_col,str(9))
                            except:
                                print("Exception! no values can be inserted there") 
                            
                        #if toggled we just change the val in the possibles list
                        else:
                            try:
                                if event.key == pygame.K_1:
                                    sudoku.changePossibles(selected_row, selected_col,str(1))
                                elif event.key == pygame.K_2:
                                     sudoku.changePossibles(selected_row, selected_col,str(2))
                                elif event.key == pygame.K_3:
                                     sudoku.changePossibles(selected_row, selected_col,str(3))
                                elif event.key == pygame.K_4:
                                     sudoku.changePossibles(selected_row, selected_col,str(4))
                                elif event.key == pygame.K_5:
                                     sudoku.changePossibles(selected_row, selected_col,str(5))
                                elif event.key == pygame.K_6:
                                     sudoku.changePossibles(selected_row, selected_col,str(6))
                                elif event.key == pygame.K_7:
                                     sudoku.changePossibles(selected_row, selected_col,str(7))
                                elif event.key == pygame.K_8:
                                     sudoku.changePossibles(selected_row, selected_col,str(8))
                                elif event.key == pygame.K_9:
                                     sudoku.changePossibles(selected_row, selected_col,str(9))
                            except:
                                print("Exception! no values can be inserted there")
                            

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if 800 <= mouse_pos[0] <= 900 and 70 <= mouse_pos[1] <= 110:
                        print("You demanded a hint")
                        sudoku.solvingIteration()
                    elif 800 <= mouse_pos[0] <= 900 and 120 <= mouse_pos[1] <= 160:
                        print("You demanded to save the game state")
                        # Save button clicked
                        sudoku.saveState()
                        # Add your code for handling the save button here
                    elif 800 <= mouse_pos[0] <= 900 and 170 <= mouse_pos[1] <= 210:
                        print("You demanded to revert the changes")
                        # Revert button clicked
                        sudoku.revertState()
                        # Add your code for handling the revert button here
                    elif 800 <= mouse_pos[0] <= 900 and 220 <= mouse_pos[1] <= 260:
                        print("You demanded a reset")
                        # Reset button clicked
                        sudoku.resetTable()
                    elif 800 <= mouse_pos[0] <= 900 and 270 <= mouse_pos[1] <= 310:
                        print("You demanded a resolution")
                        # Solve button clicked
                        sudoku.solve()

                    # Clear the window
                window.fill(WHITE)



            #we draw the game board, using more thick lines to delimit the 3x3 submatrices
            self.drawGameBoard(sudoku, board_size, cell_size, submatrix_size, window, showPossibles)


            
            font = pygame.font.Font(None, 28)
            # Draw hint button
            pygame.draw.rect(window, LIGHT_GREEN , (800, 70, 100, 40))
            text = font.render("Hint", True, BLACK)
            text_rect = text.get_rect(center=(850, 90))
            window.blit(text, text_rect)

            # Draw save state button
            pygame.draw.rect(window, LIGHT_RED , (800, 120, 100, 40))
            text = font.render("Save", True, BLACK)
            text_rect = text.get_rect(center=(850, 140))
            window.blit(text, text_rect)

            # Draw revert button
            pygame.draw.rect(window, LIGHT_RED , (800, 170, 100, 40))
            text = font.render("Revert", True, BLACK)
            text_rect = text.get_rect(center=(850, 190))
            window.blit(text, text_rect)

            # Draw reset button
            pygame.draw.rect(window, LIGHT_BLUE, (800, 220, 100, 40))
            text = font.render("Reset", True, BLACK)
            text_rect = text.get_rect(center=(850, 240))
            window.blit(text, text_rect)

            # Draw solve button
            pygame.draw.rect(window, LIGHT_BLUE , (800, 270, 100, 40))
            text = font.render("Solve", True, BLACK)
            text_rect = text.get_rect(center=(850, 290))
            window.blit(text, text_rect)

            #draw the explanation box 
            font = pygame.font.Font(None, 18)
            pygame.draw.rect(window, LIGHT_GRAY, (700, 370, 300, 250))
            lines = ['BACKSPACE to delete an insertion', 'NUM KEYS to insert a value', 'CAPSLOCK to hide/show possibles' ]
            lines += ['', 'FUNCTIONS:', 'HINT: cut the possible lists', 'SAVE: memorize current table', 'REVERT: go back to last saved table', 'RESET: go back to initialization', 'SOLVE: conclude the game for me']
            if touchPossibles:
                lines =  ['HOW TO PLAY:', "Editing possibles, not answers (TAB to switch)" ] + lines
            else:
                lines =  ['HOW TO PLAY:',"Editing numbers themselves (TAB to switch)"] + lines 

            for i, line in enumerate(lines):
                text = font.render(line, True, BLACK)
                text_rect = text.get_rect(topleft=(705, 375+i*20))
                window.blit(text, text_rect)

            


            

                    



            # Update the display
            pygame.display.flip()
