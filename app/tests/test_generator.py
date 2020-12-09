import unittest

from app.core import generator
from app.core.creator_path import CreatorPath
from app.core.generator import generate_field
from app.core.triangle_field import TriangleField


class GeneratorTest(unittest.TestCase):
    def test_count(self):
        sequence = []
        expected = 0
        actual = CreatorPath.count(sequence)
        self.assertEqual(expected, actual)
        sequence = [1, 1, 1]
        expected = len(sequence)
        actual = CreatorPath.count(sequence)
        self.assertEqual(expected, actual)

    def test_count_cells(self):
        expected = [1, 4, 9, 16]
        actual = [CreatorPath.count_cells(n) for n in range(1, 5)]
        self.assertListEqual(expected, actual)

    def test_generate_triangle_field(self):
        expected = [
            [0] * 1,
            [0] * 3,
            [0] * 5,
            [0] * 7,
            [0] * 9,
        ]
        actual = generator.generate_triangle_field(5)

        self.assertEqual(expected, actual)

    def test_empty_cells(self):
        field = TriangleField([
            [1],
            [0, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 0],
        ])

        expected = {(2, 4), (3, 6), (1, 0)}
        actual = set(CreatorPath.get_empty_cells(field))

        self.assertSetEqual(expected, actual)

    def test_generator_field(self):
        field = generate_field(3)
        start = 1
        for i in field:
            assert len(i) == start
            start += 2


if __name__ == '__main__':
    unittest.main()
