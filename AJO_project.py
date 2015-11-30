import sys
import tkinter as tk
import re

import pygame
from pygame.locals import *

from backtracking_generator import Maze, MazeRunner, AutomaticMazeRunner, TIMER_TICK_GENRATE_MAZE, \
    TIMER_TICK_MOVE_AUTOMAZERUNNER


class MazeParameters():
    def __init__(self, width, height, delay, isAutomatic):
        self.width = width
        self.height = height
        self.delay = delay
        self.isAutomatic = isAutomatic


class InputField(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.entryString = ""
        self.entry = tk.Entry(self, width=375)
        self.outputEntry = tk.Entry(self, width=375)
        self.button = tk.Button(self, text="Generate a maze and a mazerunner", command=self.on_button)
        self.entry.pack()
        self.button.pack()
        self.outputEntry.pack()
        self.geometry('450x80')

    def on_button(self):
        print("Building a maze!")
        self.entryString = self.entry.get()
        self.manipulate_the_string()

    def return_Entry(self):
        return self.entryString

    def manipulate_the_string(self):
        stringsFromEntry = self.entryString.split()

        self.outputEntry.delete(0, K_END)
        print(stringsFromEntry)
        if stringsFromEntry == []:
            self.outputEntry.insert(0, "Write something to the input field")
            return

        upperedStringsFromEntry = []
        for word in stringsFromEntry:
            upperedStringsFromEntry.append(word.upper())

        if upperedStringsFromEntry[0] != "BUILDMAZE":
            self.outputEntry.insert(0, "The first word should be buildmaze!")
            return

        widthWord = ""
        heightWord = ""
        delayWord = ""
        isAutomatic = False

        widthChecked = False
        heightChecked = False
        isDelayChecked = False
        isAutomaticChecked = False
        for word in upperedStringsFromEntry:
            print(word)

            if not widthChecked:
                if word.find("WIDTH") != -1:
                    widthWord = word
                    widthChecked = True
                else:
                    widthWord = "WIDTH15"

            if not heightChecked:
                if word.find("HEIGHT") != -1:
                    heightWord = word
                    heightChecked = True
                else:
                    heightWord = "HEIGHT10"

            if not isDelayChecked:
                if word.find("DELAY") != -1:
                    delayWord = word
                    isDelayChecked = True
                else:
                    delayWord = "DELAY1"

            if not isAutomaticChecked:
                if word.find("ISAUTOMATIC") != -1:
                    isAutomatic = True
                    isAutomaticChecked = True
                else:
                    isAutomatic = False

        width = self.getANumberValueFromWord(widthWord)
        height = self.getANumberValueFromWord(heightWord)
        delay = 0.001 * float(self.getANumberValueFromWord(delayWord))

        if width > 150 or height > 150:
            self.outputEntry.insert(0, "Values too high! Check documentation for max parameters")
            return

        if width <= 0 or height <= 0 or delay <= 0:
            self.outputEntry.insert(0, "Values too low! Check documentation for min parameters")
            return

        print(width, height, delay, isAutomatic)

        mazeParam = MazeParameters(width, height, delay, isAutomatic)

        self.generateMaze(mazeParam)

    def getANumberValueFromWord(self, word):
        return int(re.search(r'\d+', word).group())

    def generateMaze(self, mazeParameters):
        maze = Maze(mazeParameters.width, mazeParameters.height, mazeParameters.delay)
        mazeRunner = MazeRunner(maze.get_start_position()[0], maze.get_start_position()[1], mazeParameters.width,
                                mazeParameters.height)
        automaticMazeRunner = AutomaticMazeRunner(maze.get_start_position()[0], maze.get_start_position()[1],
                                                  mazeParameters.width, mazeParameters.height)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    del maze
                    sys.exit(0)
                elif event.type == TIMER_TICK_GENRATE_MAZE:
                    maze.tick()
                elif event.type == TIMER_TICK_MOVE_AUTOMAZERUNNER:
                    automaticMazeRunner.moveTick(maze)
                elif event.type == pygame.KEYUP and not mazeParameters.isAutomatic and maze.isBuilt:
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
                        print(mazeRunner.x, mazeRunner.y)
                        print(maze.get_specific_cell(mazeRunner.x, mazeRunner.y))

                    if mazeRunner.x == maze.get_end_position()[0] and mazeRunner.y == \
                            maze.get_end_position()[1]:
                        print("You won!")

                if mazeParameters.isAutomatic and maze.isBuilt:
                    pygame.time.set_timer(TIMER_TICK_MOVE_AUTOMAZERUNNER, int(mazeParameters.delay * 100))


if __name__ == "__main__":
    app = InputField()
    app.mainloop()
