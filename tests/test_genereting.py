import unittest

from numberlink_puzzle.core import triangle_field
from numberlink_puzzle.core import generator


class GeneratingTest(unittest.TestCase):
    def test_count(self):
        sequence = []
        expected = 0
        actual = generator.Generator.count(sequence)
        assert expected == actual

        sequence = [1, 1, 1]
        expected = len(sequence)
        actual = generator.Generator.count(sequence)
        assert expected == actual

    def test_count_cells(self):
        expected = [1, 4, 9, 16]
        actual = [generator.Generator.count_cells(i)
                  for i in range(1, 5)]
        self.assertListEqual(expected, actual)

    def test_generate_triangle_field(self):
        expected = [[0] * 1,
                    [0] * 3,
                    [0] * 5,
                    [0] * 7,
                    [0] * 9]
        actual = generator.Generator.generate_triangle_field(5)
        assert expected == actual

    def test_empty_cells(self):
        field = triangle_field.TriangleField([
            [1],
            [0, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 0]])

        expected = {(2, 4), (3, 6), (1, 0)}
        actual = set(generator.Generator.get_empty_cells(field))

        self.assertSetEqual(expected, actual)

    def test_generator_field(self):
        field = generator.Generator.generate_field(3)
        start = 1
        for i in field:
            assert len(i) == start
            start += 2
