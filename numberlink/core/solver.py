import itertools
from typing import List, Dict

from numberlink.core.generator import Generator
from numberlink.core.structures import Node, Segment
from numberlink.core.triangle_field import TriangleField


class Solver:
    def get_field_from_solution(self, field: TriangleField,
                                solution: List[list]) -> List[list]:
        result = TriangleField(Generator.generate_triangle_field(field.size))
        for pair in field.get_targets()['pairs']:
            start, end = tuple(pair)
            number = field[start]

            while start != end:
                for edge in solution:
                    if start in edge:
                        result[start] = number
                        start = self.opposite(start, edge)

            result[end] = number

        return result.field

    def create_solutions(self, root: Node, path: List[list] = None):
        path = path or []

        if root is Node.second_link:
            yield path
        elif root is not Node.first_second:
            yield from itertools.chain(
                self.create_solutions(root.first, path),
                self.create_solutions(root.second, path + [root.edge]))

    def solve(self, instance: TriangleField):
        graph = instance.make_graph()
        targets = instance.get_targets()
        vertices = Segment(graph.vertices())
        edges = graph.edges()
        root = Node(edges[0], {v: v for v in vertices.active}, 1)

        def get_node(node_edge: List[tuple],
                     neighbors: dict,
                     name: int) -> Node:
            if node_edge:
                return Node(node_edge, neighbors, name)

            return Node.second_link

        nodes = [root]
        while edges:
            edge = edges.pop(0)
            next_edge = edges[0] if edges else None
            self.update_vertices(vertices, edge, edges)
            new_nodes = []

            for node in nodes:
                links = []
                if self.is_first_inconsistent(node, targets, vertices):
                    links.append(Node.first_second)
                else:
                    new_neighbor = self.update_main_path(node.neighbor, vertices.active)
                    links.append(get_node(next_edge, new_neighbor, 0))
                if self.is_second_inconsistent(node, targets, vertices):
                    links.append(Node.first_second)
                else:
                    new_neighbor = self.update_main_path(
                        self.update_neighbors(node), vertices.active)
                    links.append(get_node(next_edge, new_neighbor, 1))

                new_nodes.extend(n for n in links if not self.is_link(n))
                node.add_link(*links)
            nodes = new_nodes

        return self.create_solutions(root)

    @staticmethod
    def is_first_inconsistent(node: Node,
                              targets: dict,
                              vertices: Segment) -> bool:
        nodes = (v for v in node.edge if v not in vertices.active)

        def condition(v: tuple):
            return (node.neighbor[v] == v
                    or v not in targets['vertices']
                    and node.neighbor[v] not in [0, v])

        return any(condition(v) for v in nodes)

    def is_second_inconsistent(self, node: Node,
                               targets: dict,
                               vertices: Segment) -> bool:
        union = targets['vertices'] | vertices.passive
        pair = {node.neighbor[v] for v in node.edge}

        def condition(v: tuple) -> bool:
            return (v in targets['vertices'] and node.neighbor[v] != v
                    or node.neighbor[v] in [0, self.opposite(v, node.edge)])

        return (pair <= union and pair not in targets['pairs']
                or any(condition(v) for v in node.edge))

    @staticmethod
    def is_link(node: Node) -> bool:
        return node in [Node.first_second, Node.second_link]

    def is_not_link(self, node: Node) -> bool:
        return not self.is_link(node)

    @staticmethod
    def update_main_path(neighbors: dict,
                         main_path: set) -> dict:
        return {v: neighbors[v] for v in main_path}

    def update_neighbors(self, parent: Node) -> Dict:
        neighbors = {}
        for vertex in parent.neighbor:
            if vertex in parent.edge and parent.neighbor[vertex] != vertex:
                neighbors[vertex] = 0
            elif parent.neighbor[vertex] in parent.edge:
                temp = self.opposite(parent.neighbor[vertex], parent.edge)
                neighbors[vertex] = parent.neighbor[temp]
            else:
                neighbors[vertex] = parent.neighbor[vertex]

        return neighbors

    @staticmethod
    def update_vertices(vertices: Segment,
                        edge: list,
                        edges: List[list]):
        vertices_in_edges = set(itertools.chain(*edges))
        for vertex in (v for v in edge if v not in vertices_in_edges):
            vertices.leave(vertex)

    @staticmethod
    def opposite(x: tuple, pair: List[tuple]) -> tuple:
        if x == pair[1]:
            return pair[0]
        elif x == pair[0]:
            return pair[1]
