import numpy as np
import pygame
import time
from display import AbstractDisplay
from path_finder import AbstractAstar


class Display(AbstractDisplay):
    # Implement how to draw individual object type
    def draw_cell(self, x, y, value):
        if value == 1:
            rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
            pygame.draw.rect(self.screen, (255, 165, 0), rect)
        elif value == 2:
            rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
            pygame.draw.rect(self.screen, (0, 0, 255), rect)
        elif value == 3:
            rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
            pygame.draw.rect(self.screen, (0, 255, 0), rect)
        elif value == 4:
            rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
            pygame.draw.rect(self.screen, (0, 0, 0), rect)
        elif value == 5:
            rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
            pygame.draw.rect(self.screen, (255, 0, 0), rect)
        elif value == 6:
            rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
            pygame.draw.rect(self.screen, (255, 255, 0), rect)


class Astar(AbstractAstar):
    def is_valid(self, x, y, value):
        if value == 5:
            return False
        return True

    def heuristic(self, location, destination):
        return sum(np.abs(location - destination))


def place(source, destination, location):
    destination[location[0]:location[0] + source.shape[0], location[1]:location[1] + source.shape[1]] = source


def main():
    window_size = (800, 800)
    resolution = (20, 20)

    # world as basic array
    world = np.zeros(shape=resolution, dtype=object)

    # display that maps world to a interactive world
    disp = Display(size=window_size, world=world)

    # path finding that returns path as list of ordered cell's location
    astar = Astar(world=world)

    #  SETUP OBJECTS

    # actor (initially at source)
    actor = np.ones(shape=(1, 1))

    # destination
    destination = np.empty(shape=(1, 1))
    destination.fill(3)

    # mouse
    mouse = np.empty(shape=(1, 1))
    mouse.fill(4)

    # obstacle
    obstacle = np.empty(shape=(1, 1))
    obstacle.fill(5)

    # path trace
    path_trace = np.empty(shape=(1, 1))
    path_trace.fill(6)

    # set location in world
    # actor
    actor_loc = (0, 0)
    dest_loc = (world.shape[0] - 1, world.shape[1] - 1)
    obstacles_loc = []

    start = time.time()

    while True:
        world.fill(0)

        if disp.mouse_down:
            obstacles_loc.append(disp.get_mouse_position())

        for obstacle_loc in obstacles_loc:
            place(obstacle, world, location=obstacle_loc)

        # if disp.key_down:
        path = astar.get_optimal_path(actor_loc, dest_loc)

        if path is not None:
            for trace in path:
                place(path_trace, world, trace)

        place(actor, world, location=actor_loc)
        place(destination, world, location=(world.shape[0] - 1, world.shape[1] - 1))
        place(mouse, world, disp.get_mouse_position())

        if time.time() - start > 1:
            start = time.time()
            actor_loc = path[1] if len(path) > 1 else (0, 0)

        disp.update()


if __name__ == '__main__':
    main()
