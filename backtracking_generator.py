# -*- coding: UTF-8 -*-

import pygame, sys, os, random, time
from pygame.locals import *
from cell import Cell

# ----------------------------------------------------------------------
# Aglorytm generowania labiryntu
# Autorzy: Jarosław Żok Rafał Brzychcy grzegorzwilczek
# Zmodyfikował: Bartłomiej Pokrzywiński na potrzeby pracy inżynierskiej
# Implementacja objęta jest licencją Creative Commons BY-SA 3.0 Polska.
# ----------------------------------------------------------------------

# Kolory RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (160, 160, 255)
GREEN = (160, 255, 160)
GRAY = (230, 230, 230)
ENDPOINTPURPLE = (139, 0, 139)
YELLOW = (255,255,0)


MAZE_WIDTH = 4
MAZE_HEIGHT = 5

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# GruboĹÄ linii Ĺcian
LINE_WIDTH = 3

# Czas na narysowanie kolejnych linni
DRAW_SLEEP = 0.001

# Definiujemy wĹasne zdarzenie na kaĹźde tykniÄcie zegara. W nim bÄdziemy rysowaÄ kolejne ramki animacji
TIMER_TICK_GENRATE_MAZE = pygame.USEREVENT + 1

TIMER_TICK_MOVE_AUTOMAZERUNNER = pygame.USEREVENT + 2


# OpĂłĹşnienie w milisekundach miÄdzy kolejnymi krokami algorytmu
DELAY = 1
# Numery reprezentujÄce ĹcianÄ za ktĂłrÄ znajduje siÄ sÄsiad
# 0 - na gĂłrze
# 1 - po lewej
# 2 - po prawej
# 3 - na dole
NBR_UP = 0
NBR_LEFT = 1
NBR_RIGHT = 2
NBR_DOWN = 3


class MazeRunnerBase:
    def __init__(self, x,y,mazeWidth = MAZE_WIDTH,mazeHeight = MAZE_HEIGHT):
        self.x = x
        self.y = y
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.window = pygame.display.set_mode((WINDOW_WIDTH + LINE_WIDTH, WINDOW_HEIGHT + LINE_WIDTH))
        self.brickwidth = (WINDOW_WIDTH + (WINDOW_WIDTH % self.mazeWidth)) / self.mazeWidth
        self.brickheight = (WINDOW_HEIGHT + (WINDOW_HEIGHT % self.mazeHeight)) / self.mazeHeight

    def moveDown(self):
        self.change_location(1, 0)

    def moveUp(self):
        self.change_location(-1, 0)

    def moveLeft(self):
        self.change_location(0, -1)

    def moveRight(self):
        self.change_location(0, 1)

    def draw_cell(self, cell, color=WHITE):
        xpos = self.brickwidth * cell[0]
        ypos = self.brickheight * cell[1]
        pygame.draw.rect(self.window, color, (
            xpos + LINE_WIDTH, ypos + LINE_WIDTH, self.brickwidth - LINE_WIDTH, self.brickheight - LINE_WIDTH))

    def getLocation(self):
        return self.location

    def change_location(self, moveHeight, moveWidth,color = WHITE):
        if self.x + moveWidth < 0:
            self.x = 0
        elif self.y + moveHeight < 0:
            self.y = 0
        elif self.x + moveWidth > self.mazeWidth - 1:
            self.x = self.mazeWidth - 1
        elif self.y + moveHeight > self.mazeHeight - 1:
            self.y = self.mazeHeight - 1
        else:
            self.draw_cell([self.x,self.y], color)
            self.x += moveWidth
            self.y += moveHeight
            self.draw_cell([self.x,self.y], RED)
        pygame.display.update()


class AutomaticMazeRunner(MazeRunnerBase):
    def __init__(self, x,y,mazeWidth = MAZE_WIDTH,mazeHeight = MAZE_HEIGHT):
        super().__init__(x,y,mazeWidth,mazeHeight)
        self.visited = []

    def draw_cell(self, cell, color=BLACK):
        xpos = self.brickwidth * cell[0]
        ypos = self.brickheight * cell[1]
        pygame.draw.rect(self.window, color, (
            xpos + LINE_WIDTH, ypos + LINE_WIDTH, self.brickwidth - LINE_WIDTH, self.brickheight - LINE_WIDTH))

    def moveAcrossTheMazeInRandomDirection(self, currentCell):
            self.visited.append(currentCell)
            whereToGo = random.randint(0,3)

            if(whereToGo == 0 and not currentCell.hasNorthWall()):
                self.moveUp()
            if(whereToGo == 1 and not currentCell.hasSouthWall()):
                self.moveDown()
            if(whereToGo == 2 and not currentCell.hasWestWall()):
                self.moveLeft()
            if(whereToGo == 3 and not currentCell.hasEastWall()):
                self.moveRight()

    def change_location(self, moveHeight, moveWidth,color = YELLOW):
        super().change_location(moveHeight,moveWidth,color)

    def moveTick(self,maze):
        if self.x != maze.get_end_position()[0] or self.y != maze.get_end_position()[1]:
            currentCell = maze.get_specific_cell(self.x,self.y)
            self.moveAcrossTheMazeInRandomDirection(currentCell)
        else:
            print("Random maze runner had met the end")
            pygame.time.set_timer(TIMER_TICK_MOVE_AUTOMAZERUNNER, 0)  # Zatrzymujemy timer





class MazeRunner(MazeRunnerBase):
    pass


class Maze(object):
    '''
	Klasa implementujÄca labirynt. Przechowuje stan komĂłrek labiryntu i realizuje algorytm Backtracking
	'''

    def __init__(self, width, height,delay = DRAW_SLEEP):
        random.seed()

        self.i = 0
        self.stack = []
        self.unvisited = []
        self.visited = []
        self.isBuilt = False
        # Ograniczenie podanej wielkoĹci labiryntu do MAX_WIDTH i MAX_HEIGHT
        self.width = width
        self.height = height
        self.delay = delay

        # Inicjalizacja silnika
        pygame.init()

        # Otwarcie okna z szarym tĹem
        self.window = pygame.display.set_mode((int(WINDOW_WIDTH + LINE_WIDTH), int(WINDOW_HEIGHT + LINE_WIDTH)))
        pygame.display.set_caption('Labirynt backtracking')
        self.window.fill(GRAY)

        # Wyliczamy i zapamiÄtujemy wielkoĹÄ komnaty w pikselach
        # szerokoĹÄ komnaty w pikselach to szerokoĹÄ okna w pikselach + reszta z dzielenia szerokoĹci okna w pikselach
        # przez iloĹÄ komnat podzielone przez iloĹÄ komnat
        # Podobne wyliczenie nastÄpuje dla wysokoĹci komnaty
        self.brickwidth = (WINDOW_WIDTH + (WINDOW_WIDTH % self.width)) / self.width
        self.brickheight = (WINDOW_HEIGHT + (WINDOW_HEIGHT % self.height)) / self.height

        # Losujemy poczÄtkowÄ komnatÄ labiryntu, od niej zaczynamy rysowanie
        self.start = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        self.end = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        self.cells = [[Cell(y, x, [1, 1, 1, 1]) for x in range(self.width)] for y in range(self.height)]

        # Rysujemy linie poziome
        for y in range(self.height):
            time.sleep(self.delay)
            pygame.draw.line(self.window, BLACK, (0, y * self.brickheight), (WINDOW_WIDTH, y * self.brickheight),
                             LINE_WIDTH)

            pygame.display.update()

        pygame.draw.line(self.window, BLACK, (0, WINDOW_HEIGHT), (WINDOW_WIDTH, WINDOW_HEIGHT), LINE_WIDTH)
        pygame.display.update()

        # Rysujemy linie pionowe
        for x in range(self.width):
            time.sleep(self.delay)
            pygame.draw.line(self.window, BLACK, (x * self.brickwidth, 0), (x * self.brickwidth, WINDOW_HEIGHT),
                             LINE_WIDTH)
            pygame.display.update()

        pygame.draw.line(self.window, BLACK, (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), LINE_WIDTH)
        pygame.display.update()

        # Tworzymy komnatÄ labiryntu dla kaĹźdego x i y
        for x in range(self.width):
            for y in range(self.height):
                cell = (x, y)
                if cell == self.start:  # Komnata startowa jest rysowana na czerwono, ustawiamy przy okazji, Ĺźe jest juĹź odwiedzona
                    self.current = cell
                    self.visited.append(cell)
                else:
                    self.stack.append(cell)
                self.unvisited.append(cell)

        self.draw_cell(self.start, RED)
        pygame.display.update()

        # Ustawienie timera na 2ms
        pygame.time.set_timer(TIMER_TICK_GENRATE_MAZE, int(delay*1000))

    def __del__(self):
        '''
	  Metoda klasy wywowĹywana, gdy obiekt jest niszczony (destruktor klasy). Sprawdzamy czy okno jest otwarte
	  i jeĹźeli tak to koĹczymy pracÄ z bibliotekÄ pygame.
	  '''
        if self.window:
            pygame.quit()

    def get_neighbours(self, cell):
        def fine(v, s):
            if 0 <= v < s:
                return True
            return False

        nbrs = []
        for n in (cell[0] - 1, cell[1], NBR_LEFT), (cell[0], cell[1] - 1, NBR_UP), (cell[0] + 1, cell[1], NBR_RIGHT), (
                cell[0], cell[1] + 1, NBR_DOWN):
            if (n[0], n[1]) not in self.visited and fine(n[0], self.width) and fine(n[1],
                                                                                    self.height):
                nbrs.append(n)
        random.shuffle(nbrs)

        return nbrs

    def make_visited(self, cell):
        cell = (cell[0], cell[1])
        try:
            i = self.unvisited.index(cell)
            self.visited.append(cell)
            del self.unvisited[i]
        except ValueError:
            pass

    def get_specific_cell(self, x, y):
        return self.cells[y][x]

    def draw_cell(self, cell, color=WHITE):
        xpos = self.brickwidth * cell[0]
        ypos = self.brickheight * cell[1]
        pygame.draw.rect(self.window, color, (
            xpos + LINE_WIDTH, ypos + LINE_WIDTH, self.brickwidth - LINE_WIDTH, self.brickheight - LINE_WIDTH))

    def wreck_wall(self, neighbours, color=GRAY):
        '''
	Metoda burzy ĹcianÄ miÄdzy komnatami podanymi jako lista w parametrze neighbours.
	Wylicza na podstawie wartoĹci numeru sÄsiada, ktĂłrÄ ĹcianÄ wyburzyÄ i jÄ usuwa.
	Usuwanie polega na narysowaniu linii w kolorze tĹa w miejscu, gdzie znajduje siÄ
	Ĺciana miÄdzy podanymi sÄsiadami.
	'''
        x ,y  = neighbours[0][0], neighbours[0][1]

        if neighbours[1][2] == NBR_LEFT:
            p1 = x, y
            p2 = x, y + 1
            p1 = ((p1[0] * self.brickwidth), (p1[1] * self.brickheight) + LINE_WIDTH)
            p2 = ((p2[0] * self.brickwidth), (p2[1] * self.brickheight) - LINE_WIDTH)
            self.draw_line_if_points_are_in_the_window(color, p1, p2, [y, x], NBR_LEFT)

        elif neighbours[1][2] == NBR_UP:
            p1 = x, y
            p2 = x + 1, y
            p1 = ((p1[0] * self.brickwidth) + LINE_WIDTH, (p1[1] * self.brickheight))
            p2 = ((p2[0] * self.brickwidth) - LINE_WIDTH, (p2[1] * self.brickheight))
            self.draw_line_if_points_are_in_the_window(color, p1, p2, [y, x], NBR_UP)

        elif neighbours[1][2] == NBR_RIGHT:
            p1 = x + 1, y
            p2 = x + 1, y + 1
            p1 = ((p1[0] * self.brickwidth), (p1[1] * self.brickheight) + LINE_WIDTH)
            p2 = ((p2[0] * self.brickwidth), (p2[1] * self.brickheight) - LINE_WIDTH)
            self.draw_line_if_points_are_in_the_window(color, p1, p2, [y, x], NBR_RIGHT)

        elif neighbours[1][2] == NBR_DOWN:
            p1 = x, y + 1
            p2 = x + 1, y + 1
            p1 = ((p1[0] * self.brickwidth) + LINE_WIDTH, (p1[1] * self.brickheight))
            p2 = ((p2[0] * self.brickwidth) - LINE_WIDTH, (p2[1] * self.brickheight))
            self.draw_line_if_points_are_in_the_window(color, p1, p2, [y, x], NBR_DOWN)

        print(self.cells)

    def draw_line_if_points_are_in_the_window(self, color, p1, p2, setCell, wallDestroyMask):
        if (0 < p1[0] < WINDOW_WIDTH and 0 < p2[0] < WINDOW_WIDTH) and (
                            0 < p2[1] < WINDOW_HEIGHT and 0 < p2[1] < WINDOW_HEIGHT):
            pygame.draw.line(self.window, color, p1, p2, LINE_WIDTH)

            if wallDestroyMask == NBR_LEFT:
                self.cells[setCell[0]][setCell[1]].destroyWestWall()
                self.cells[setCell[0]][setCell[1] - 1].destroyEastWall()

            if wallDestroyMask == NBR_UP:
                self.cells[setCell[0]][setCell[1]].destroyNorthWall()
                self.cells[setCell[0] - 1][setCell[1]].destroySouthWall()

            if wallDestroyMask == NBR_RIGHT:
                self.cells[setCell[0]][setCell[1]].destroyEastWall()
                self.cells[setCell[0]][setCell[1] + 1].destroyWestWall()

            if wallDestroyMask == NBR_DOWN:
                self.cells[setCell[0]][setCell[1]].destroySouthWall()
                self.cells[setCell[0] + 1][setCell[1]].destroyNorthWall()

    def tick(self):
        '''
	Metoda realizuje wĹaĹciwy algorytm. KaĹźde jej wywoĹanie to jeden krok algorytmu.
	Jest ona wywoĹywana za kaĹźdym razem kiedy timer odliczy liczbÄ milisekund zawartÄ w
	zmiennej DELAY
	'''
        if self.stack:
            neighbours = self.get_neighbours(self.current)
            if neighbours:
                cell = neighbours[0]

                self.stack.append(self.current)

                if (cell[0], cell[1]) == self.start:  # o
                    self.draw_cell(cell, RED)
                else:
                    self.draw_cell(cell, GREEN)

                self.wreck_wall((self.current, cell), BLUE)
                self.current = cell
                self.make_visited(cell)
            elif self.stack:
                if self.current == self.start:
                    self.draw_cell(self.current, RED)
                else:
                    self.draw_cell(self.current, GRAY)

                cell = self.stack.pop()
                self.current = cell  #

            else:
                cell = self.unvisited[
                    random.randint(0, len(self.unvisited) - 1)]
                self.current = cell
                self.make_visited(cell)

            pygame.display.update()  # Odrysowujemy zawartoĹÄ okna
        else:
            print("Zrobione!")  # Stos jest juĹź pusty, koniec algorytmu
            self.isBuilt=True
            self.draw_cell(self.end, ENDPOINTPURPLE)
            pygame.display.update()
            pygame.time.set_timer(TIMER_TICK_GENRATE_MAZE, 0)  # Zatrzymujemy timer

    def get_start_position(self):
        return self.start

    def get_end_position(self):
        return self.end


if __name__ == "__main__":
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    mazeRunner = MazeRunner(maze.get_start_position()[0],maze.get_start_position()[1])
    automaticMazeRunner = AutomaticMazeRunner(maze.get_start_position()[0],maze.get_start_position()[1])
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                del maze
                sys.exit(0)
            elif event.type == TIMER_TICK_GENRATE_MAZE:
                maze.tick()
            elif event.type == TIMER_TICK_MOVE_AUTOMAZERUNNER:
                automaticMazeRunner.moveTick(maze)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    if not maze.get_specific_cell(mazeRunner.x, mazeRunner.y).hasNorthWall():
                        mazeRunner.moveUp()
                    else:
                        print("I CANNOT MOVE THROUGH WALLS DAMMIT")

                if event.key == pygame.K_s:
                    if not maze.get_specific_cell(mazeRunner.x, mazeRunner.y).hasSouthWall():
                        mazeRunner.moveDown()
                    else:
                        print("I CANNOT MOVE THROUGH WALLS DAMMIT")

                if event.key == pygame.K_a:
                    if not maze.get_specific_cell(mazeRunner.x, mazeRunner.y).hasWestWall():
                        mazeRunner.moveLeft()
                    else:
                        print("I CANNOT MOVE THROUGH WALLS DAMMIT")

                if event.key == pygame.K_d:
                    if not maze.get_specific_cell(mazeRunner.x, mazeRunner.y).hasEastWall():
                        mazeRunner.moveRight()
                    else:
                        print("I CANNOT MOVE THROUGH WALLS DAMMIT")

                if event.key == pygame.K_5:
                    print(mazeRunner.x,mazeRunner.y)
                    print(maze.get_specific_cell(mazeRunner.x, mazeRunner.y))

                if mazeRunner.x == maze.get_end_position()[0] and mazeRunner.y == \
                        maze.get_end_position()[1]:
                    print("You won!")

                if event.key == pygame.K_1:
                    pygame.time.set_timer(TIMER_TICK_MOVE_AUTOMAZERUNNER, DELAY)

