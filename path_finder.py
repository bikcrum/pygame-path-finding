import numpy as np
from tqdm import tqdm


class Node:
    def __init__(self, parent, location):
        self.parent = parent
        self.location = location
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return np.all(self.location == other.location)


class AbstractAstar:
    def __init__(self, world):
        self.world = world
        pass

    def _trace_path(self, current_node):
        path = []
        node = current_node
        while node is not None:
            path.append(node)
            node = node.parent

        # reverse list so that it's from start to end
        return path[::-1]

    def get_optimal_path(self, source, destin):

        start_node = Node(None, source)
        end_node = Node(None, destin)

        open_list = []
        closed_list = []

        open_list.append(start_node)

        iterations = 0
        max_iterations = sum(self.world.shape) ** 10

        while open_list:
            iterations += 1
            print(iterations)

            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            if iterations > max_iterations:
                return self._trace_path(current_node)

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                return self._trace_path(current_node)

            children = np.array(
                [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]) + current_node.location

            children = children[np.all((children >= [0, 0]) & (children < self.world.shape), axis=1)]

            children = map(lambda x: Node(current_node, x), children)

            for child in children:
                if not self.is_valid(child.location[0], child.location[1],
                                     self.world[child.location[0], child.location[1]]):
                    continue

                if child in closed_list:
                    continue

                child.g = current_node.g + self.cost_to_child()
                child.h = self.heuristic(child.location, end_node.location)

                child.f = child.g + child.h

                skip = False
                for i, node in enumerate(open_list):
                    if child == node and node.f < child.f:
                        skip = True
                        break

                if skip:
                    continue

                open_list.append(child)

    def cost_to_child(self):
        raise NotImplementedError('You must implement cost_to_child function')

    def is_valid(self, x, y, value):
        raise NotImplementedError('You must implement is_valid function')

    def heuristic(self, location, destination):
        raise NotImplementedError('You must implement heuristic function')
