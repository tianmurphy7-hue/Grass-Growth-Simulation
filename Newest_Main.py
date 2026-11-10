import pygame
import numpy as np
import random

class Grid:
    def __init__(self, Width, Height, CellSize):
        self.Width = Width
        self.Height = Height
        self.Depth = 3
        self.CellSize = CellSize

        self.Cells = np.zeros((self.Depth, Height, Width), dtype=int)

        pygame.init()
        pygame.display.set_caption('Simulation')
        self.Screen = pygame.display.set_mode((Width * CellSize, Height * CellSize))

        self.Blue = (85, 170, 210)

        self.Greens = [
            (190, 185, 110),  # 0 - Pale, dry grass (least healthy)
            (155, 175, 65),  # 1 - Yellowish grass
            (125, 165, 45),  # 2 - Dull green
            (95, 155, 35),  # 3 - Light green
            (65, 145, 30),  # 4 - Medium green
            (45, 130, 25),  # 5 - Healthy green
            (30, 115, 25),  # 6 - Rich green
            (20, 100, 25),  # 7 - Deep green
            (15, 85, 20),  # 8 - Very healthy green
            (5, 65, 15)  # 9 - Dark, lush green (healthiest)
        ]

    def DrawCells(self):
        self.Screen.fill((0, 0, 0))

        for Y in range (len(self.Cells[0])):
            for X in range (len(self.Cells[0][Y])):
                if self.Cells[2][Y][X] == 0:
                    pygame.draw.rect(self.Screen, self.Greens[max(self.Cells[0][Y][X],0)], pygame.Rect(X * self.CellSize, Y * self.CellSize, self.CellSize, self.CellSize))
                else:
                    pygame.draw.rect(self.Screen, self.Blue, pygame.Rect(X * self.CellSize, Y * self.CellSize, self.CellSize, self.CellSize))

        pygame.display.update()

    def CheckNeighborWaterLevels(self, X, Y):
        if (0 <= X < self.Width and 0 <= Y < self.Height):
            return self.Cells[0][Y][X]
        else:
            return None

    def CheckNeighborWaterChange(self, X, Y):
        if (0 <= X < self.Width and 0 <= Y < self.Height):
            return self.Cells[1][Y][X]
        else:
            return None

    def CheckValidNeighbor(self, X, Y):
        if (0 <= X < self.Width and 0 <= Y < self.Height):
            return True
        else:
            return False

    def ExchangeWithNeighbor(self, X1, Y1, X2, Y2):
        if not self.CheckValidNeighbor(X2, Y2):
            return #Blank

        if self.Cells[2][Y2][X2] == 1:
            self.Cells[1][Y1][X1] += 1
            return #Blank

        if random.random() < 0.35:
            return #Blank

        NeighborWaterLevels = self.CheckNeighborWaterLevels(X2, Y2)
        NeighborWaterChange = self.CheckNeighborWaterChange(X2, Y2)

        if (NeighborWaterLevels != None and NeighborWaterLevels >= 2 * self.Cells[0][Y1][X1] and NeighborWaterLevels + NeighborWaterChange > 1):
            Exchange = random.randint(1, 2)
            self.Cells[1][Y2][X2] -= Exchange
            self.Cells[1][Y1][X1] += Exchange
            return  # Blank

    def SpreadWaterLevels(self):
        for Y in range (len(self.Cells[0])):
            for X in range (len(self.Cells[0][Y])):

                self.ExchangeWithNeighbor(X, Y, X + 1, Y + 1)  # Down-right
                self.ExchangeWithNeighbor(X, Y, X + 1, Y - 1)  # Up-right
                self.ExchangeWithNeighbor(X, Y, X - 1, Y + 1)  # Down-left
                self.ExchangeWithNeighbor(X, Y, X - 1, Y - 1)  # Up-left

                self.ExchangeWithNeighbor(X, Y, X + 1, Y)  # Right
                self.ExchangeWithNeighbor(X, Y, X - 1, Y)  # Left
                self.ExchangeWithNeighbor(X, Y, X, Y + 1)  # Down
                self.ExchangeWithNeighbor(X, Y, X, Y - 1)  # Up

        for Y in range (len(self.Cells[0])):
            for X in range (len(self.Cells[0][Y])):
                if self.Cells[2][Y][X] == 0:
                    self.Cells[0][Y][X] = min(max(self.Cells[0][Y][X] + self.Cells[1][Y][X], 0), 9)

                    if random.random() < 0.075 and self.Cells[0][Y][X] > 0:
                        self.Cells[0][Y][X] -= 1

        self.Cells[1] = 0

    def Reset(self):
        self.Cells = np.zeros((self.Depth, self.Height, self.Width), dtype=int)


def InitializeGame():
    for i in range(35):
        grid.Cells[2][random.randint(0, 34)][random.randint(0, 59)] = 1

    grid.DrawCells()
    pygame.time.delay(1400)


Clock = pygame.time.Clock()

grid = Grid(60, 35, 25)

InitializeGame()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                grid.Reset()
                InitializeGame()

    grid.SpreadWaterLevels()
    grid.DrawCells()

    pygame.time.delay(700)
