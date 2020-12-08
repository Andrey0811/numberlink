import itertools
from typing import List, Set, Dict

from app.algorithms.generator import generate_triangle_field
from app.algorithms.structures import Node, Segment
from app.numberlink import TriangleLink, TriangleField


def get_right_path(edge, paths):
    for path in paths:
        if any(v in path for v in edge):
            return path

    return None


def get_field_from_solution(field: TriangleLink,
                            solution: List[List]) -> List[List]:
    result = TriangleField(generate_triangle_field(field.size))
    for pair in field.get_targets()['pairs']:
        start, end = tuple(pair)
        number = field[start]

        while start != end:
            for edge in solution:
                if start in edge:
                    result[start] = number
                    start = opposite(start, edge)

        result[end] = number

    return result.field


def create_solutions(root: Node, path: List[List[tuple]] = None):
    path = path or []

    if root is Node.second_link:
        yield path
    elif root is not Node.first_second:
        yield from itertools.chain(
            create_solutions(root.first, path),
            create_solutions(root.second, path + [root.edge]))


def get_path(path: List[List[tuple]], node: Node):
    return path if node.name == 0 else path + [node.edge]


def solve(instance: TriangleLink):
    graph = instance.make_graph()
    targets = instance.get_targets()
    vertices = Segment(graph.vertices())
    edges = graph.edges()
    root = Node(edges[0], {v: v for v in vertices.active}, 1)

    def get_node(node_edge: List[tuple],
                 neighbors: Dict[tuple, tuple],
                 name: int) -> Node:
        if node_edge:
            return Node(node_edge, neighbors, name)

        return Node.second_link

    nodes = [root]
    while edges:
        edge = edges.pop(0)
        next_edge = edges[0] if edges else None
        update_vertices(vertices, edge, edges)
        new_nodes = []

        for node in nodes:
            links = []
            if is_first_inconsistent(node, targets, vertices):
                links.append(Node.first_second)
            else:
                new_neighbor = update_main_path(node.neighbor, vertices.active)
                links.append(get_node(next_edge, new_neighbor, 0))
            if is_second_inconsistent(node, targets, vertices):
                links.append(Node.first_second)
            else:
                new_neighbor = update_main_path(
                    update_neighbors(node), vertices.active)
                links.append(get_node(next_edge, new_neighbor, 1))

            new_nodes.extend(n for n in links if not is_link(n))
            node.add_link(*links)
        nodes = new_nodes

    return create_solutions(root)


def is_first_inconsistent(node: Node,
                          targets: Dict[str, Set[tuple]],
                          vertices: Segment) -> bool:
    nodes = (v for v in node.edge if v not in vertices.active)

    def condition(v: tuple):
        return (node.neighbor[v] == v
                or v not in targets['vertices']
                and node.neighbor[v] not in [0, v])

    return any(condition(v) for v in nodes)


def is_second_inconsistent(node: Node,
                           targets: Dict[str, Set[tuple]],
                           vertices: Segment) -> bool:
    union = targets['vertices'] | vertices.passive
    pair = {node.neighbor[v] for v in node.edge}

    def condition(v: tuple) -> bool:
        return (v in targets['vertices'] and node.neighbor[v] != v
                or node.neighbor[v] in [0, opposite(v, node.edge)])

    return (pair <= union and pair not in targets['pairs']
            or any(condition(v) for v in node.edge))


def is_link(node: Node) -> bool:
    return node in [Node.first_second, Node.second_link]


def is_not_link(node: Node) -> bool:
    return not is_link(node)


def update_main_path(neighbor: Dict[tuple, tuple],
                     main_path: Set[tuple]) -> dict:
    return {v: neighbor[v] for v in main_path}


def update_neighbors(parent: Node) -> Dict[tuple, tuple]:
    neighbors = {}
    for vertex in parent.neighbor:
        if vertex in parent.edge and parent.neighbor[vertex] != vertex:
            neighbors[vertex] = 0
        elif parent.neighbor[vertex] in parent.edge:
            temp = opposite(parent.neighbor[vertex], parent.edge)
            neighbors[vertex] = parent.neighbor[temp]
        else:
            neighbors[vertex] = parent.neighbor[vertex]

    return neighbors


def update_vertices(vertices: Segment,
                    edge: List[tuple],
                    edges: List[List[tuple]]):
    vertices_in_edges = set(itertools.chain(*edges))
    for vertex in (v for v in edge if v not in vertices_in_edges):
        vertices.leave(vertex)


def opposite(x: tuple, pair: List[tuple]) -> tuple:
    if x == pair[1]:
        return pair[0]
    elif x == pair[0]:
        return pair[1]
