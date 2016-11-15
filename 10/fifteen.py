"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

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
        # replace with your code
        stat2 = True
        stat3 = True
        stat1 = (self.get_number(target_row,target_col) == 0)
        for index in range(target_col + 1, self.get_width()):
            if self.get_number(target_row , index) != target_row*self.get_width() + index:
                stat2 = False
                break
        #print self.get_number(target_row,target_row)
        for row in range(target_row+1, self.get_height()):
            for col in range(0 , self.get_width()):
                if self.get_number(row,col) != row*self.get_width() + col:
                    stat3 = False
                    break
        return stat1 and stat2 and stat3
    
    def get_move_string(self,target_row,target_col,value):
        '''
        move the tile with value to the target position with the 
        zero tile on the left.
        '''
        move_string = []
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == value:
                    num_pos = [row, col]
        #move vertically
        move_string.append('u'*(target_row - num_pos[0]))
        #move horizontally
        if target_col > num_pos[1]:
            move_string.append('l'*(target_col - num_pos[1]))
            num_pos[1] = num_pos[1] + 1
            if num_pos[0] != target_row:
                #move the tile right by x unit
                move_string.append('drrul'*(target_col - num_pos[1]))
                #get to the top of the tile and plus one unit
                move_string.append('dru')
                num_pos[0] = num_pos[0] + 1
                #move the tile down by x unit
                move_string.append('lddru'*(target_row - num_pos[0]))
                move_string.append('ld')
            elif target_row != 0:
                move_string.append('urrdl'*(target_col - num_pos[1]))
            else:
                move_string.append('drrul'*(target_col - num_pos[1]))
        elif target_col < num_pos[1]:
            move_string.append('r'*(num_pos[1] - target_col))
            num_pos[1] = num_pos[1] - 1
            #move the tile left by x unit
            if num_pos[0] > 0:
                move_string.append('ulldr'*(num_pos[1] - target_col))
                #get to the top of the tile
                move_string.append('ul')
            else:
                move_string.append('dllur'*(num_pos[1] - target_col))
                #get to the top of the tile
                move_string.append('dlu')
                num_pos[0] = num_pos[0] + 1
            #move the tile down by x unit
            move_string.append('lddru'*(target_row - num_pos[0]))
            move_string.append('ld')
        else:
            num_pos[0] = num_pos[0] + 1
            #move the tile down by x unit
            move_string.append('lddru'*(target_row - num_pos[0]))
            move_string.append('ld')
        return "".join(move_string)
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        value = target_row*self.get_width() + target_col
        move_string = self.get_move_string(target_row,target_col,value)
        move_string = "".join(move_string)
        self.update_puzzle(move_string)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        num_to_place = target_row*self.get_width()
        move_string = []
        if self.get_number(target_row - 1,0) == num_to_place:
            move_string.append('u')
            move_string.append('r'*(self.get_width() - 1))
            move_string = "".join(move_string)
            self.update_puzzle(move_string)
            return move_string
        move_string.append('ur')
        self.update_puzzle('ur')
        move_string.append(self.get_move_string(target_row - 1 , 1 , num_to_place))
        self.update_puzzle(self.get_move_string(target_row - 1 , 1 , num_to_place))
        move_string.append('ruldrdlurdluurddlu')
        self.update_puzzle('ruldrdlurdluurddlu')
        move_string.append('r'*(self.get_width() - 1))
        self.update_puzzle('r'*(self.get_width() - 1))
        move_string = "".join(move_string)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(0,target_col) != 0:
            return False
        if self.get_number(1,target_col) != 1*self.get_width() + target_col:
            return False
        for row in range(2,self.get_height()):
            for col in range(0,target_col + 1):
                if self.get_number(row , col) != row*self.get_width() + col:
                    return False
        for row in range(0,self.get_height()):
            for col in range(target_col + 1 , self.get_width()):
                if self.get_number(row , col) != row*self.get_width() + col:
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(1,target_col) != 0:
            return False
        for row in range(2,self.get_height()):
            for col in range(0,target_col + 1):
                if self.get_number(row , col) != row*self.get_width() + col:
                    return False
        for row in range(0,self.get_height()):
            for col in range(target_col + 1 , self.get_width()):
                if self.get_number(row , col) != row*self.get_width() + col:
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        num_pos = list(self.current_position(0,target_col))
        move_string = ''
        if num_pos[1] == target_col - 1 and num_pos[0] == 0:
            self.update_puzzle('ld')
            return 'ld'
        elif num_pos[1] == target_col - 2 and num_pos[0] == 0:
            self.update_puzzle('dluldrruld')
            return 'dluldrruld'
        else:
            move_string += 'l'*(target_col - num_pos[1])
            if num_pos[0] == 0:
                num_pos[1] += 1
                move_string += 'drrul' * (target_col - num_pos[1] - 2)
                move_string += 'drru'
            else:
                move_string += 'd'
                if target_col - num_pos[1] - 2 < 0:
                    move_string += 'lur'
                elif target_col - num_pos[1] - 2 > 0:
                    num_pos[0] -= 1
                    move_string += 'rul'
                    num_pos[1] += 1
                    move_string += 'drrul' * (target_col - num_pos[1] - 2)
                    move_string += 'drru'
                else:
                    move_string += 'ru'
            move_string += 'rdluldrruld'
            self.update_puzzle(move_string)
            return move_string
                
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        value = self.get_width() + target_col
        move_string = self.get_move_string(1,target_col,value)
        move_string = move_string+'ur'
        self.update_puzzle(move_string)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        move_string += "ul"
        times = 0
        self.update_puzzle('ul')
        while self.lower_row_invariant(0,0) == False:
            times += 1
            move_string += "drul"
            self.update_puzzle('drul')
            if times == 3:
                break
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ''
        if not self.lower_row_invariant(self._height-1,self._width-1):
            num_pos = self.current_position(0,0)
            move_string += 'r'*(self._width-1-num_pos[1])
            move_string += 'd'*(self._height-1-num_pos[0])
            self.update_puzzle(move_string)
            
        for row in range(self._height-1,1,-1):
            for col in range(self._width-1,-1,-1):
                if col > 0 and row > 1:
                    assert self.lower_row_invariant(row,col)
                    move_string += self.solve_interior_tile(row,col)
                    assert self.lower_row_invariant(row,col-1)
                elif col == 0 and row > 1:
                    assert self.lower_row_invariant(row,col)
                    move_string += self.solve_col0_tile(row)
                    assert self.lower_row_invariant(row-1,self._width-1)
        for col in range(self._width-1,-1,-1):
            for row in range(1,-1,-1):
                if col > 1 and row == 1:
                    assert self.row1_invariant(col)
                    move_string += self.solve_row1_tile(col)
                    assert self.row0_invariant(col)
                elif col > 1 and row == 0:
                    assert self.row0_invariant(col)
                    move_string += self.solve_row0_tile(col)
                    assert self.row1_invariant(col-1)
                elif col < 1:
                    move_string += self.solve_2x2()
                    return move_string

# Start interactive simulation
puzzle = Puzzle(10,10)
poc_fifteen_gui.FifteenGUI(puzzle)
