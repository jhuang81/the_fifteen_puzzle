"""
THE FRAME OF THIS CODE IS PROVIDED BY COURSE: PRINCIPLE OF COMPUTING
            OFFERED BY RICE UNIVERSITY ON COURSERA
PLAY THE GAME HERE: http://www.codeskulptor.org/#user37_L1Z2yQJS4W_3.py

Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import codeskulptor

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # check whether self._grid[target_row][target_col] == 0
        parameter1 = self._grid[target_row][target_col] == 0
        #print parameter1
        # check all row from i + 1 is sloved
        parameter2 = True
        init_val = self.get_height() * self.get_width() - 1        
        for dummy_row in range(self.get_height() - target_row - 1):
            for dummy_col in range(self.get_width()):
                boolean_check = self._grid[self.get_height() - dummy_row - 1][self.get_width() - dummy_col - 1] == init_val
                parameter2 = parameter2 and boolean_check
                init_val = init_val - 1

        # check all tiles from j + 1 in row i is sloved
        parameter3 = True
        for dummy_col in range(self.get_width() - target_col - 1):
            bollean_check = self._grid[target_row][self.get_width() - dummy_col - 1] == init_val
            parameter3 = parameter3 and bollean_check
            init_val = init_val - 1
        return parameter1 and parameter2 and parameter3

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        row_convert = {False:'u', True: 'd'}
        col_convert = {False:'l', True: 'r'}
        move = ''
        current_pos = self.current_position(target_row, target_col)
        current_row = current_pos[0]
        current_col = current_pos[1]
        row_0 = target_row
        col_0 = target_col
        
        # move the 0 up above the file, (if the file is in row 0, move across the file)
        clone_puzzle = self.clone()
        if current_row == 0 or (current_col == col_0):
            move_row = current_row - row_0
            move_col = current_col - col_0
            move = move + row_convert[move_row > 0] * (abs(move_row)-1) + col_convert[move_col > 0] * abs(move_col) + 'u'
        else:
            move_row = current_row - row_0 - 1
            move_col = current_col - col_0
            move = move + row_convert[move_row > 0] * abs(move_row) + col_convert[move_col > 0] * abs(move_col)            
        clone_puzzle.update_puzzle(move)

        # move the file to the same col as target file
        current_col = clone_puzzle.current_position(target_row, target_col)[1]
        while current_col != target_col:
            if current_col < target_col:
                move = move + 'rdlur'
                clone_puzzle.update_puzzle('rdlur')
            if current_col > target_col:
                move = move + 'ldrul'
                clone_puzzle.update_puzzle('ldrul')
            current_col = clone_puzzle.current_position(target_row, target_col)[1]

        # move the file to the same row as target file
        assert clone_puzzle.current_position(0, 0)[1] == clone_puzzle.current_position(target_row, target_col)[1]
        current_row = clone_puzzle.current_position(target_row, target_col)[0]
        while current_row != target_row:
            #print current_row, target_row
            move = move + 'lddru'
            clone_puzzle.update_puzzle('lddru')
            current_row = clone_puzzle.current_position(target_row, target_col)[0]

        # move the 0 to the next file
        move = move + 'ld'
        clone_puzzle.update_puzzle('ld')		
        
        assert clone_puzzle.lower_row_invariant(target_row, target_col - 1)
        self.update_puzzle(move)
        return move

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        row_convert = {False:'u', True: 'd'}
        col_convert = {False:'l', True: 'r'}
        move = ''
        clone_puzzle = self.clone()
        
        # make the file in the 2 * 2 file above the target file
        if clone_puzzle.current_position(target_row, 0)[1] > 1:       
            move_row = clone_puzzle.current_position(target_row, 0)[0] - target_row
            move_col = clone_puzzle.current_position(target_row, 0)[1] - 1
            move = move + row_convert[move_row > 0] * abs(move_row) + col_convert[move_col > 0] * abs(move_col)
            clone_puzzle.update_puzzle(move)

            while clone_puzzle.current_position(target_row,0)[1] > 1:
                if clone_puzzle.current_position(target_row,0)[0] == target_row -1:
                    move = move + 'rulld'
                    clone_puzzle.update_puzzle('rulld')
                else:
                    move = move + 'rdllu'
                    clone_puzzle.update_puzzle('rdllu')

        
        if clone_puzzle.current_position(target_row, 0)[0] < target_row - 2:
            current_row = clone_puzzle.current_position(target_row, 0)[0]
            current_col = clone_puzzle.current_position(target_row, 0)[1]
            move_row = current_row - clone_puzzle.current_position(0, 0)[0] + 1
            move_col = current_col - clone_puzzle.current_position(0, 0)[1]
            current_move = row_convert[move_row > 0] * abs(move_row) + col_convert[move_col > 0] * abs(move_col)

            move = move + current_move
            clone_puzzle.update_puzzle(current_move)

            while clone_puzzle.current_position(target_row,0)[0] < target_row - 2:
                move = move + 'urddl'
                clone_puzzle.update_puzzle('urddl')
                
        move_row = target_row - clone_puzzle.current_position(0, 0)[0]
        move_col = 0 - clone_puzzle.current_position(0, 0)[1]
        current_move =  col_convert[move_col > 0] * abs(move_col) + row_convert[move_row > 0] * abs(move_row)      
        move = move + current_move
        clone_puzzle.update_puzzle(current_move)                
       
        
        # make the file on the right side of target file move to the target file, with the file on the 2 * 2 file above it
        if clone_puzzle.current_position(target_row, 0) == (target_row - 1, 1):
            move = move + 'uurdld'
            clone_puzzle.update_puzzle('uurdld')
        move = move + 'ru'
        clone_puzzle.update_puzzle('ru')
        
        # make the file move to the file above the target file
        assert clone_puzzle.current_position(target_row, 1)[1] == 0
        while clone_puzzle.current_position(target_row, 0) != (target_row - 1, 0):             
            move = move + 'lurd'
            clone_puzzle.update_puzzle('lurd')
       
        # move the two file to the target place
        move = move + 'dlur'
        clone_puzzle.update_puzzle('dlur')
        
        # mvoe the 0 to the next target file
        move = move + (self.get_width() - 2) * 'r'
        clone_puzzle.update_puzzle((self.get_width() - 2) * 'r')        
        
        assert clone_puzzle.lower_row_invariant(target_row - 1, self.get_width() - 1)
        self.update_puzzle(move)           
        return move

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check whether self._grid[0][target_col] == 0
        row0_is_zero = self._grid[0][target_col] == 0

        # check all row from i + 2 is sloved
        row_after_is_solved = True
        init_val = self.get_height() * self.get_width() - 1        
        for dummy_row in range(self.get_height() - 2):
            for dummy_col in range(self.get_width()):
                boolean_check = self._grid[self.get_height() - dummy_row - 1][self.get_width() - dummy_col - 1] == init_val
                row_after_is_solved = row_after_is_solved and boolean_check
                init_val = init_val - 1
                
        # check all tiles from j in row 1 is sloved
        tiles_in_row1_is_solved = True
        for dummy_col in range(self.get_width() - target_col):
            bollean_check = self._grid[1][self.get_width() - dummy_col - 1] == init_val
            tiles_in_row1_is_solved = tiles_in_row1_is_solved and bollean_check
            init_val = init_val - 1
 
        # check all tiles from j + 1 in row 0 is sloved
        tiles_in_row0_is_sloved = True
        init_val = self.get_width() - 1
        for dummy_col in range(self.get_width() - target_col - 1):
            bollean_check = self._grid[0][self.get_width() - dummy_col - 1] == init_val
            tiles_in_row0_is_sloved = tiles_in_row0_is_sloved and bollean_check
            init_val = init_val - 1
 
        return row0_is_zero and row_after_is_solved and tiles_in_row1_is_solved and tiles_in_row0_is_sloved        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check whether self._grid[1][target_col] == 0
        parameter1 = self._grid[1][target_col] == 0
 
        # check all row from 2 is sloved
        parameter2 = True
        init_val = self.get_height() * self.get_width() - 1        
        for dummy_row in range(self.get_height() - 2):
            for dummy_col in range(self.get_width()):
                boolean_check = self._grid[self.get_height() - dummy_row - 1][self.get_width() - dummy_col - 1] == init_val
                parameter2 = parameter2 and boolean_check
                init_val = init_val - 1
 
        # check all tiles from j + 1 in row 1 is sloved
        parameter3 = True
        for dummy_col in range(self.get_width() - target_col - 1):
            bollean_check = self._grid[1][self.get_width() - dummy_col - 1] == init_val
            parameter3 = parameter3 and bollean_check
            init_val = init_val - 1
        parameter4 = True
        init_val = self.get_width() - 1
        for dummy_col in range(self.get_width() - target_col - 1):
            bollean_check = self._grid[0][self.get_width() - dummy_col - 1] == init_val
            parameter4 = parameter4 and bollean_check
            init_val = init_val - 1
        return parameter1 and parameter2 and parameter3 and parameter4      

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # move 0 to the file
        move = ''
        clone_puzzle = self.clone()
        row_convert = {False:'u', True: 'd'}
        col_convert = {False:'l', True: 'r'}
        # move the 0 file to the position of the file         
        row_0 = clone_puzzle.current_position(0, 0)[0]
        col_0 = clone_puzzle.current_position(0, 0)[1]
        move_row = clone_puzzle.current_position(0, target_col)[0] - row_0
        move_col = clone_puzzle.current_position(0, target_col)[1] - col_0 
        current_move =  col_convert[move_col > 0] * abs(move_col) + row_convert[move_row > 0] * abs(move_row)
        move = move + current_move
        clone_puzzle.update_puzzle(current_move)

        #assert clone_puzzle.current_position(0, target_col)[0] == 0     
        # move 0 file on the left side of the file (if the file is in col 0, move it to col 1)
        if clone_puzzle.current_position(0, target_col)[1] == 0:
            move = move + 'ruldr'
            clone_puzzle.update_puzzle('ruldr')
        if clone_puzzle.current_position(0, target_col)[1] == clone_puzzle.current_position(0,0)[1]:
            move = move + 'lu'
            clone_puzzle.update_puzzle('lu')
        
        # move the file into the file on the left side of target file
        while  target_col - clone_puzzle.current_position(0, target_col)[1] > 1:
            move = move + 'drrul'
            clone_puzzle.update_puzzle('drrul')
            
        # move the file to the file (0, target_col -2) file, move the file below the target file to the right side of the file
        # move the two file back to the target places
        if clone_puzzle.current_position(0, target_col) != (0, target_col):
            move = move + 'r' + 'rdlur' + 'lldrrul' 
            clone_puzzle.update_puzzle('r' + 'rdlur' + 'lldrrul')
        
        #  move the 0 to the next target place
        move = move + 'd'
        clone_puzzle.update_puzzle('d')        
        self.update_puzzle(move)
        return move

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move = ''
        clone_puzzle = self.clone()
        row_convert = {False:'u', True: 'd'}
        col_convert = {False:'l', True: 'r'}
        
        # move the 0 file to the position of the file
        current_pos = clone_puzzle.current_position(1, target_col)
        current_row = current_pos[0]
        current_col = current_pos[1]
        row_0 = clone_puzzle.current_position(0, 0)[0]
        col_0 = clone_puzzle.current_position(0, 0)[1]
        move_row = current_row - row_0
        move_col = current_col - col_0 
        current_move = row_convert[move_row > 0] * abs(move_row) + col_convert[move_col > 0] * abs(move_col)

        move = move + current_move
        clone_puzzle.update_puzzle(current_move)
        
        # mvoe the file to the row 1
        while clone_puzzle.current_position(1, target_col)[0] != 1:
            move = move + 'druld'
            clone_puzzle.update_puzzle('druld')
        assert clone_puzzle.current_position(1, target_col)[0] == 1
        
        # move the file to the the target file
        while clone_puzzle.current_position(1, target_col)[1] != target_col:
            move = move + 'urrdl'
            clone_puzzle.update_puzzle('urrdl')
        
        # move the 0 to the next target
        if not clone_puzzle.row0_invariant(target_col):
            move = move + 'ur'
        self.update_puzzle(move)
        return move

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move = ''
        clone_puzzle = self.clone()
        # check if already solved
        if clone_puzzle.row0_invariant(0):
            return move
        
        # move the 0 to the target place
        assert clone_puzzle.row1_invariant(1)
        move = move + 'ul'
        clone_puzzle.update_puzzle('ul')
        
        while not clone_puzzle.row0_invariant(0):
            move = move + 'drul'
            clone_puzzle.update_puzzle('drul')
        
        self.update_puzzle(move)
        return move

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move = ''
        clone_puzzle = self.clone()
        start = False
        row_convert = {False:'u', True: 'd'}
        col_convert = {False:'l', True: 'r'}
            
        # phase1, find the point to begin, move the 0 to the point to satisfy the invariant, solve the phase 1
        phase12_list = []
        phase_row = range(2, self.get_height())
        phase_col = range(self.get_width())
        phase_row.reverse()
        phase_col.reverse()
        for dummy_row in phase_row:
            for dummy_col in phase_col:
                phase12_list.append((dummy_row, dummy_col))
                        
        # phase 2, find the point to begin, move 0 to the start, solve phase 2
        phase_col = range(2, self.get_width())
        phase_col.reverse()
        for dummy_col in phase_col:
            phase12_list.append((1, dummy_col))
            phase12_list.append((0, dummy_col))
                          
        for dummy_file in phase12_list:
            if clone_puzzle.current_position(dummy_file[0], dummy_file[1]) != dummy_file:
                    start = True
            if start:
                if clone_puzzle.current_position(0, 0) != dummy_file:                                        
                    move_row = dummy_file[0] - clone_puzzle.current_position(0, 0)[0]
                    move_col = dummy_file[1] - clone_puzzle.current_position(0, 0)[1]
                    current_move =  col_convert[move_col > 0] * abs(move_col) + row_convert[move_row > 0] * (abs(move_row))                
                    clone_puzzle.update_puzzle(current_move)
                    move = move + current_move

                if dummy_file[0] == 0:
                    #assert clone_puzzle.row0_invariant(dummy_file[1])
                    current_move = clone_puzzle.solve_row0_tile(dummy_file[1])

                if dummy_file[0] == 1:
                    #assert clone_puzzle.row1_invariant(dummy_file[1])
                    current_move = clone_puzzle.solve_row1_tile(dummy_file[1])
 
                    #assert clone_puzzle.lower_row_invariant(dummy_file[0], dummy_file[1])
                if (dummy_file[1] == 0) and (dummy_file[0] != 0 and dummy_file[0] != 1):
                    current_move = clone_puzzle.solve_col0_tile(dummy_file[0])
                if (dummy_file[1] != 0) and (dummy_file[0] != 0 and dummy_file[0] != 1):
                    current_move = clone_puzzle.solve_interior_tile(dummy_file[0], dummy_file[1])
                move = move + current_move                
        
        # phase 3 
        if not clone_puzzle.row0_invariant(0):
            move_row = 1 - clone_puzzle.current_position(0, 0)[0]
            move_col = 1 - clone_puzzle.current_position(0, 0)[1]
            current_move = row_convert[move_row > 0] * (abs(move_row)-1) + col_convert[move_col > 0] * abs(move_col)                
            clone_puzzle.update_puzzle(current_move)
            move = move + current_move
            move = move + clone_puzzle.solve_2x2()
      
        self.update_puzzle(move)
        return move




