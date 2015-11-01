class Cell(object):
    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        # Walls - [NORTH,SOUTH,WEST,EAST] 1 means wall is there 0  means wall is not there
        self.walls = walls

    def hasNorthWall(self):
        return self.walls[0] == 1

    def hasSouthWall(self):
        return self.walls[1] == 1

    def hasWestWall(self):
        return self.walls[2] == 1

    def hasEastWall(self):
        return self.walls[3] == 1

    def destroyNorthWall(self):
        self.walls[0] = 0

    def destroySouthWall(self):
        self.walls[1] = 0

    def destroyWestWall(self):
        self.walls[2] = 0

    def destroyEastWall(self):
        self.walls[3] = 0

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.walls)

    def __repr__(self, *args, **kwargs):
        return self.__str__()

    def set_Walls(self,value):
        self.walls = value;

    def get_Walls(self):
        return self.walls

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self,value):
        self.x = value

    def set_y(self,value):
        self.y = value
