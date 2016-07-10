"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = [0]*len(line)
    result1 = [0]*len(line)
    
    index = 0
    for num in line:
        if num != 0:
            result[index] = num
            index += 1
    
    for num in range(len(result) - 1):
        if result[num] == result[num+1]:
            result[num] *= 2
            result[num + 1] = 0
    
    index = 0
    for num in result:
        if num != 0:
            result1[index] = num
            index += 1
            
    return result1


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, _grid_height, _grid_width):
        # replace with your code
        self._grid_height = _grid_height
        self._grid_width = _grid_width
        self._grid = [[0*row + 0*col for row in range(self._grid_width)] 
                     for col in range(self._grid_height)]
    def reset(self):
        """
        Reset the game so the _grid is empty except for two
        initial tiles.
        """
        self._grid = [[0*row + 0*col for row in range(self._grid_width)] 
                     for col in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the _grid for debugging.
        """
        
        return str(self._grid)

    def get__grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get__grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # all check the map
        start_cells = {UP:[[0,col] for col in range(self._grid_width)],
                     DOWN:[[self._grid_height - 1,col] for col in range(self._grid_width)],
                     LEFT:[[row,0] for row in range(self._grid_height)],
                     RIGHT:[[row , self._grid_width - 1] for row in range(self._grid_height)]}
        steps = {UP:self._grid_height,
                DOWN:self._grid_height,
                RIGHT:self._grid_width,
                LEFT:self._grid_width}
        
        for cell in start_cells[direction]:
            temp_list = []
            for step in range(steps[direction]):
                row = cell[0] + step * OFFSETS[direction][0]
                col = cell[1] + step * OFFSETS[direction][1]
                temp_list.append(self.get_tile(row,col))
            temp_list = merge(temp_list)
            for step in range(steps[direction]):
                row = cell[0] + step * OFFSETS[direction][0]
                col = cell[1] + step * OFFSETS[direction][1]
                self.set_tile(row,col,temp_list[step])
        #self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        num = -1
        positoin_dict = {}
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                value = self.get_tile(row,col)
                if value == 0:
                    num += 1
                    positoin_dict[num] = [row,col]
                    
        if random.random() > 0.9:
            new_value = 4
        else:
            new_value = 2
        if num < 0:
            return
        new_position = positoin_dict[random.randrange(num)]
        
        self.set_tile(new_position[0] , new_position[1] , new_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(5, 5))
