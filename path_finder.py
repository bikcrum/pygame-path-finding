import numpy as np
from tqdm import tqdm


class Node:
    def __init__(self, location):
        self.location = location
        self.f = 0
        self.g = 0
        self.h = 0


class AbstractAstar:
    def __init__(self, world):
        self.world = world
        pass

    def get_optimal_path(self, source, destin):
        open_list = []
        closed_list = []

        start = Node(location=source)
        end = Node(location=destin)

        open_list.append(start)

        while open_list:
            min_node = None
            min_node_index = None
            # find node with minimum f
            for i in range(len(open_list)):
                if min_node is None or open_list[i].f < min_node.f:
                    min_node = open_list[i]
                    min_node_index = i

            open_list = open_list[:min_node_index] + open_list[min_node_index + 1:]

            neighbours = np.array(
                [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]) + min_node.location

            neighbours = neighbours[np.all((neighbours >= [0, 0]) & (neighbours < self.world.shape), axis=1)]

            successors = [Node(neighbour) for neighbour in neighbours]

            for successor in successors:
                if not self.is_valid(successor.location[0], successor.location[1],
                                     self.world[successor.location[0], successor.location[1]]):
                    continue
                if np.all(successor.location == end.location):
                    closed_list.append(min_node)
                    return [node.location for node in closed_list]
                else:
                    successor.g = min_node.g + 1
                    successor.h = self.heuristic(successor.location, destin)
                    successor.f = successor.g + successor.h

                skip = False
                for node in open_list:
                    if np.all(node.location == successor.location) and node.f < successor.f:
                        skip = True
                        break
                if skip:
                    continue

                skip = False
                for node in closed_list:
                    if np.all(node.location == successor.location) and node.f < successor.f:
                        skip = True
                        break

                if not skip:
                    open_list.append(successor)

            closed_list.append(min_node)

        return [node.location for node in closed_list]

    def is_valid(self, x, y, value):
        raise NotImplementedError('You must implement is_valid function')

    def heuristic(self, location, destination):
        raise NotImplementedError('You must implement heuristic function')
