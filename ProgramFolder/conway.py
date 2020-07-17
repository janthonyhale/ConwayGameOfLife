"""
    To run:
        pip3 install pygame (Just to install pygame)
        (Another method to install)
        python3 -m pip install pygame
        python3 conway.py < filename
        (Try python3 conway.py < data/generator.dat)
    Description:
        This file runs a simulate of Conway's game of life
    Author: James Hale (janthonyhale@gmail.com)
    Date: 15 July 2020
"""

# Imports
import pygame
import fileinput
import random


class Environment:
    def __init__(self, size, living):
        """
            Constructor method for Environment
        :param size: Tuple of the size of the environment (x, y)
        :param living: x, y coordinates of the living cells at time zero
        """
        self.width = size[0]  # Width and height of the board
        self.height = size[1]
        if living is None:
            self.board, self.alive = self.random_init()
        else:
            row = [0] * self.width  # Init board
            self.board = list()
            for _ in range(self.height):
                self.board.append(list(row))
            self.alive = living  # List that holds locations of all alive cells
            # Initialize the population
            for l in self.alive:
                self.insert(l)

    def __call__(self, *args, **kwargs):
        """
            Call method, generates the board at the next turn
        :param args:
        :param kwargs:
        :return: void
        """
        tmp = list()
        for row in self.board:
            tmp.append(list(row))
        tmp_alive = list()  # To hold the alive values in the next turn
        for c in self.alive:  # Iterate through alive cells
            alive_neighbors = 0  # Keep track of this
            for n in ((c[0] + i, c[1] + j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0):
                # Iterate through neighbors
                if 0 <= n[0] < self.height and 0 <= n[1] < self.width and self.board[n[0]][n[1]]:
                    alive_neighbors += 1  # Our neighbor is alive
                elif 0 <= n[0] < self.height and 0 <= n[1] < self.width and not tmp[n[0]][n[1]]:
                    # Our neighbor is dead; maybe they'll come to life!
                    alive_neighbors_n = 0
                    for nn in ((n[0] + i, n[1] + j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0):
                        # Going through our neighbor's neighbors
                        if 0 <= nn[0] < self.height and 0 <= nn[1] < self.width and self.board[nn[0]][nn[1]]:
                            # They are alive in the same way
                            alive_neighbors_n += 1
                    if alive_neighbors_n == 3:
                        # Populated, this cell will come alive
                        tmp[n[0]][n[1]] = 1
                        tmp_alive.append(n)
            if not 2 <= alive_neighbors <= 3:  # This cell has died of over-crowding or starvation
                tmp[c[0]][c[1]] = 0
            else:
                tmp_alive.append(c)
        self.alive = tmp_alive
        self.board = tmp

    def insert(self, location):
        """
            Make a cell alive
        :param location: x, y location
        :return: void
        """
        if 0 <= location[0] <= self.height and 0 <= location[1] < self.width:
            self.board[location[0]][location[1]] = 1

    def random_init(self, seed_=1):
        """
            Randomly initializes the board
        :return: Random grid of dead/alive cells, spaces of alive cells
        """
        random.seed(seed_)
        tmp_board = list()
        tmp_alive = list()
        for i in range(self.height):
            tmp_board.append(list())
            for j in range(self.width):
                tmp = random.randint(0, 1)
                tmp_board[-1].append(tmp)  # Random of either being alive or dead
                if tmp:
                    tmp_alive.append((i, j))
        return tmp_board, tmp_alive

    def print_board(self):
        """
            Prints the board: 0 -> dead, 1 -> alive
        :return: void
        """
        for i in self.board:
            print(i)


class Viewer:
    def __init__(self, env, window_size):
        """
            Constructor
        :param env:
        """
        self.environment = env
        self.size = window_size
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")

    def __call__(self, *args, **kwargs):
        """
            Update the pygame window
        :param args:
        :param kwargs:
        :return:
        """
        self.screen.fill((0, 0, 0))
        w = self.size[0] / self.environment.width
        h = self.size[1] / self.environment.height
        for i in range(self.environment.height):
            pygame.draw.line(self.screen, (25, 84, 0), (0, h * i), (self.size[0], h * i))
            for j in range(self.environment.width):
                if not i:
                    pygame.draw.line(self.screen, (25, 84, 0), (w * j, 0), (w * j, self.size[1]))
                if self.environment.board[i][j] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), [w * j, h * i, w, h])

    def run(self):
        """
            Run the simulation
        :return: void
        """
        done = False
        while not done:
            self.environment()
            self()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.clock.tick(30)
            pygame.display.flip()


def read_file():
    """
        Reads the file
    :param shift: x and y shift
    :return: size of board, living cell locations
    """
    tmp = list()
    for i in (line.split() for line in fileinput.input()):
        if i[0] == "r":
            return tmp[0], None
        tmp.append((int(i[0]), int(i[1])))
    return tmp[0], tmp[1:]


def main():
    """
        Main program: execution stems from here
    :return: void
    """
    window_size = [750, 750]
    size, life = read_file()
    env = Environment(size, life)
    win = Viewer(env, window_size)
    win.run()


if __name__ == "__main__":
    # Run main program
    main()

# End File
