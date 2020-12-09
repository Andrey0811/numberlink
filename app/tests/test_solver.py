import unittest

from graph_tools import Graph

from app.core import solver
from app.core.structures import Node
from app.core.triangle_field import TriangleField


class SolverTest(unittest.TestCase):
    def setUp(self):
        self.field1 = TriangleField([[1],
                                     [1, 0, 2],
                                     [3, 0, 3, 0, 2]])
        self.field2 = TriangleField([[1],
                                     [1, 0, 2],
                                     [1, 0, 3, 0, 2],
                                     [3, 0, 0, 0, 4, 0, 4]])
        self.field3 = TriangleField([[1],
                                     [1, 0, 2]])

        self.graph = Graph(directed=False)
        self.graph.add_edge('a', 'b')
        self.graph.add_edge('a', 'c')
        self.graph.add_edge('c', 'b')
        self.graph.add_edge('b', 'd')

    def test_update_neighbors(self):
        self.method_tester(
            expected={'a': 'b',
                      'b': 'a',
                      'c': 'c',
                      'd': 'd'},
            parent_node=Node(
                self.graph.edges()[0],
                {v: v for v in self.graph.vertices()},
                1),
            main_path=list('abcd'))

        self.method_tester(
            expected={'b': 'c',
                      'c': 'b',
                      'd': 'd'},
            parent_node=Node(
                self.graph.edges()[1],
                {'a': 'b',
                 'b': 'a',
                 'c': 'c',
                 'd': 'd'},
                1),
            main_path=list('bcd'))

        self.method_tester(
            expected={'b': 0,
                      'd': 'd'},
            parent_node=Node(
                self.graph.edges()[2],
                {'b': 'a',
                 'c': 'c',
                 'd': 'd'},
                1),
            main_path=list('bd'))

    def method_tester(self, expected, parent_node, main_path):
        actual = solver.update_main_path(
            solver.update_neighbors(parent_node), main_path)
        self.assertDictEqual(expected, actual)

    def test_solve(self):
        expected = [[(0, 0), (1, 1)], [(1, 0), (1, 1)],
                    [(1, 2), (2, 3)], [(2, 0), (2, 1)],
                    [(2, 1), (2, 2)], [(2, 3), (2, 4)]]
        actual = list(solver.solve(self.field1))
        self.assertTrue(len(actual) == 64)
        self.assertListEqual(expected, actual[0])

        expected = []
        actual = list(solver.solve(self.field2))
        self.assertListEqual(expected, actual)

        actual = list(solver.solve(self.field3))
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
