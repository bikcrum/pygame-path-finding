import numpy as np
import pygame
import sys
import time


class AbstractDisplay:
    def __init__(self, size, world):
        self.size = np.array(size)
        self.world = world
        self.block_size = self.size // self.world.shape
        self._init()

    def _init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.mouse_down = False
        self.key_down = False

    def _draw_gridlines(self):
        width, height = self.size
        block_width, block_height = self.block_size

        for x in range(0, width, block_width):
            for y in range(0, height, block_height):
                rect = pygame.Rect(x, y, *self.block_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def get_mouse_position(self):
        mouse_loc = pygame.mouse.get_pos()
        return np.array(mouse_loc) // self.block_size

    def get_pseudo_position(self, coordinate):
        return np.ceil(np.array(coordinate) // self.block_size) * self.block_size

    def _draw_world(self):
        for x in range(self.world.shape[0]):
            for y in range(self.world.shape[1]):
                self.draw_cell(x, y, self.world[x, y])

    def update(self, delay=None):
        self.screen.fill((255, 255, 255))
        self._draw_gridlines()
        self._draw_world()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == pygame.KEYDOWN:
                self.key_down = True
            elif event.type == pygame.KEYUP:
                self.key_down = False

        pygame.display.update()
        if delay is not None:
            time.sleep(delay)

    def draw_cell(self, x, y, value):
        raise NotImplementedError('Must implement draw_cell')
