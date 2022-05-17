import numpy as np
from queue import PriorityQueue


# import ray

# ray.init()


class Node:
    def __init__(self, parent, location):
        self.parent = parent
        self.location = location
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return np.all(self.location == other.location)

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f'{self.f, self.g, self.h, self.location}'


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

        open_list = PriorityQueue()
        closed_list = []

        open_list.put((start_node.f, start_node))

        iterations = 0
        max_iterations = sum(self.world.shape) ** 10

        while not open_list.empty():
            iterations += 1
            print(iterations)

            p, current_node = open_list.get()

            if iterations > max_iterations:
                return self._trace_path(current_node)

            closed_list.append(current_node)

            if current_node == end_node:
                return self._trace_path(current_node)

            # find all children (8-way)
            children = np.array(
                [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]) + current_node.location

            # discard children out of bound
            children = children[np.all((children >= [0, 0])
                                       & (children < self.world.shape), axis=1)]

            # discard children is not valid (eg. block)
            children = children[self.is_valid(children)]

            # convert children into a node pointing to parent
            children = map(lambda x: Node(current_node, x), children)

            for child in children:
                if child in closed_list:
                    continue

                child.g = current_node.g + self.cost_to_child()
                child.h = self.heuristic(child.location, end_node.location)

                child.f = child.g + child.h

                skip = False
                for _, node in open_list.queue:
                    if child == node:
                        if node.f < child.f:
                            skip = True
                        break

                if skip:
                    continue

                open_list.put((child.f, child))

    def cost_to_child(self):
        raise NotImplementedError('You must implement cost_to_child function')

    def is_valid(self, nodes):
        raise NotImplementedError('You must implement is_valid function')

    def heuristic(self, location, destination):
        raise NotImplementedError('You must implement heuristic function')
