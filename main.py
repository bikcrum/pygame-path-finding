import numpy as np
import pygame
import time
from display import AbstractDisplay
from path_finder import AbstractAstar


class Display(AbstractDisplay):
    # Implement how to draw individual object type
    def draw_cell(self, x, y, value):
        if type(value) == float:
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
        elif type(value) == tuple:
            if value[0] == 6:
                rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], *self.block_size)
                pygame.draw.rect(self.screen, (255, 255, 0), rect)
                text_surface = self.font.render(value[1], False, (0, 0, 0))
                self.screen.blit(text_surface, (x * self.block_size[0], y * self.block_size[1]))


class Astar(AbstractAstar):
    def is_valid(self, nodes):
        return self.world[nodes[:, 0], nodes[:, 1]] != 5

    def heuristic(self, location, destination):
        return sum(np.abs(location - destination))

    def cost_to_child(self):
        return 1


def place(source, destination, location):
    destination[location[0]:location[0] + source.shape[0], location[1]:location[1] + source.shape[1]] = source


def main():
    resolution = (20, 20)
    window_size = (800, 800)

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

    # set location of actor and dest
    actor_loc = (0, 0)
    dest_loc = (world.shape[0] - 1, world.shape[1] - 1)
    obstacles_loc = [(1, 1)]

    start = time.time()

    while True:
        world.fill(0)

        if disp.mouse_down:
            obstacles_loc.append(disp.get_mouse_position())

        for obstacle_loc in obstacles_loc:
            place(obstacle, world, location=obstacle_loc)

        # if disp.key_down:
        path = astar.get_optimal_path(actor_loc, dest_loc)
        # p = list(map(lambda x:x.location, path))
        if path is not None:
            for trace in path:
                path_trace = np.empty(shape=(1, 1), dtype=object)
                path_trace[0, 0] = (6, f'f={trace.f}, g={trace.g}, h={trace.h}')
                # path_trace[0, 0] = (6, '')
                place(path_trace, world, trace.location)

        place(actor, world, location=actor_loc)
        place(destination, world, location=dest_loc)
        place(mouse, world, disp.get_mouse_position())

        if time.time() - start > 0.5 and path is not None and len(path) > 1:
            start = time.time()
            # actor_loc = path[1].location

        disp.update()


if __name__ == '__main__':
    main()
