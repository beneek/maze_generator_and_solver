import random
from cell import Cell

random.seed()
MAZE_WIDTH = 16
MAZE_HEIGHT = 10

# Numery reprezentujÄ?ce Å?cianÄ? za ktÃ³rÄ? znajduje siÄ? sÄ?siad
# 0 - na gÃ³rze
# 1 - po lewej
# 2 - po prawej
# 3 - na dole
NBR_UP = 0
NBR_LEFT = 1
NBR_RIGHT = 2
NBR_DOWN = 3


class Maze(object):
    def __init__(self, mazeWidth, mazeHeight):
        self.width = mazeWidth
        self.height = mazeHeight
        self.start = Cell([random.randint(0, self.mazeWidth - 1), random.randint(0, self.mazeHeight - 1)])
        self.stack = []
        self.unvisited = []

    def generateMaze(self):
        self.mazeList = [[Cell(x, y, True) for x in range(self.mazeWidth)] for y in range(self.mazeHeight)]
        print(self.start)

        for i in self.mazeList:
            print(i)


if __name__ == '__main__':
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    maze.generateMaze()


class Cell(object):
    def __init__(self, x, y, isWall):
        self.x = x
        self.y = y
        self.isWall = isWall
