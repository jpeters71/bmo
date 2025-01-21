class SmartGrid:

    def __init__(self, width, height):
        """2D grid of zeros used to track if snake collides with its tail

        Usage: self.occupied[coords] = True
               if self.occupied[coords] is True
        """
        self.width = width
        self.height = height
        self.grid = [[False for i in range(height)]
                     for j in range(width)]

    def __getitem__(self, coords):
        if coords[0] < 0 or coords[1] < 0 or \
                coords[0] >= self.width or coords[1] >= self.height:
            return True
        return self.grid[int(coords[0])][int(coords[1])]

    def __setitem__(self, coords, value):
        if coords[0] < 0 or coords[1] < 0 or \
                coords[0] >= self.width or coords[1] >= self.height:
            return
        self.grid[int(coords[0])][int(coords[1])] = value