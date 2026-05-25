import random
import pygame
from config import CELL_SIZE
from utils import random_position

class Snake:
    def __init__(self, color, start_pos, direction):
        self.color = color
        self.body = [start_pos]
        self.direction = direction
        self.grow = False
        self.alive = True
        self.score = 0

    def move(self):
        if not self.alive:
            return

        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self, screen):
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * CELL_SIZE,
                segment[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, self.color, rect)

    def eat(self):
        self.grow = True
        self.score += 1
        


class Food:
    def __init__(self):
        self.position = random_position()

    def respawn(self, snakes):
        while True:
            pos = random_position()
            if all(pos not in snake.body for snake in snakes):
                self.position = pos
                break

    def draw(self, screen):
        rect = pygame.Rect(
            self.position[0] * CELL_SIZE,
            self.position[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (255, 0, 0), rect)