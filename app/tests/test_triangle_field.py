import unittest

from graph_tools import Graph

from app.core.triangle_field import TriangleField


class TriangleFieldTest(unittest.TestCase):
    def setUp(self):
        self.field = TriangleField([[1],
                      [1, 0, 2],
                      [1, 0, 3, 0, 2],
                      [3, 0, 0, 0, 4, 0, 4]])
        self.simple_field = TriangleField([[1],
                                           [1, 0, 2],
                                           [3, 0, 3, 0, 2]])

    def test_get_neighbours(self):
        expected = {(1, 1)}
        self.assert_neighbours(expected, (0, 0))

        expected = {(0, 0), (1, 2), (1, 0)}
        self.assert_neighbours(expected, (1, 1))

        expected = {(3, 1)}
        self.assert_neighbours(expected, (3, 0))

        expected = {(3, 5)}
        self.assert_neighbours(expected, (3, 6))

        expected = {(2, 1), (3, 3), (2, 3)}
        self.assert_neighbours(expected, (2, 2))

    def assert_neighbours(self, expected, position):
        actual = set(self.field.get_neighbours(*position))
        self.assertSetEqual(expected, actual)

    def test_check_field_when_ok(self):
        self.assertEqual(self.field.field,
                         TriangleField(self.field.field).field)

    def test_init_when_wrong(self):
        field = [[0, 0],
                 [0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]

        self.assertRaises(ValueError, TriangleField, field)
        self.assertRaises(ValueError, TriangleField, [])
        self.assertRaises(ValueError, TriangleField, None)

    def test_index_checker(self):
        self.assertFalse(self.field.is_valid(0, 1))
        self.assertFalse(self.field.is_valid(5, 0))
        self.assertFalse(self.field.is_valid(0, 3))

    def test_get_targets(self):
        expected = dict(vertices={(0, 0), (1, 0),
                                  (2, 0), (1, 2),
                                  (2, 4), (2, 2)},
                        pairs={frozenset({(0, 0), (1, 0)}),
                               frozenset({(2, 2), (2, 0)}),
                               frozenset({(1, 2), (2, 4)})})
        actual = self.simple_field.get_targets()

        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
