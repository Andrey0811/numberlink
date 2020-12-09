import unittest

from app.core import generator
from app.core.creator_path import CreatorPath
from app.core.triangle_field import TriangleField


class CreatorPathTest(unittest.TestCase):
    def setUp(self):
        field = generator.generate_triangle_field(5)
        self.constructor = CreatorPath(TriangleField(field))
        self.field = TriangleField(field)

    def test_count_busy_neighbours(self):
        self.assert_count_busy_neighbours(0, (2, 1))

        field = self.field
        field[2, 0] = field[1, 1] = 1
        self.assert_count_busy_neighbours(1, (2, 1))

        field = self.field
        field[0, 0] = field[1, 0] = field[1, 1] = 1
        self.assert_count_busy_neighbours(2, (1, 1))

    def assert_count_busy_neighbours(self, expected, pos):
        constructor = CreatorPath(self.field)
        actual = constructor.count_busy_neighbours(pos)
        self.assertEqual(expected, actual)

    def test_count_number_neighbours(self):
        actual = self.constructor.count_number_neighbours((0, 0), 1)
        self.assertEqual(0, actual)

        self.field[0, 0] = 2
        self.assert_count_numbered_neighbours(0, (0, 1), 1)

        self.field[0, 0] = self.field[1, 1] = 1
        self.assert_count_numbered_neighbours(1, (1, 1), 1)

    def assert_count_numbered_neighbours(self, expected, position, number):
        constructor = CreatorPath(self.field)
        actual = constructor.count_number_neighbours(position, number)
        self.assertEqual(expected, actual)

    def test_isolated(self):
        self.assertFalse(
            CreatorPath(self.field).is_isolated((0, 0), 1, False))

        self.field[1, 0] = self.field[1, 1] = 1
        self.field[1, 2] = self.field[0, 0] = 1
        self.assertFalse(
            CreatorPath(self.field).is_isolated((0, 0), 1, True))
        self.assertFalse(
            CreatorPath(self.field).is_isolated((0, 0), 2, False))

        self.field[1, 0] = self.field[1, 1] = 1
        self.field[1, 2] = self.field[0, 0] = 1
        self.field[0, 0] = self.field[1, 2] = 1
        self.field[2, 1] = self.field[2, 2] = 1
        self.assertTrue(
            CreatorPath(self.field).is_isolated((1, 1), 1, True))
        self.assertTrue(
            CreatorPath(self.field).is_isolated((1, 1), 2, False))

    def test_has_isolated_empty_cell(self):
        self.field[0, 0] = self.field[1, 1] = 1
        self.field[1, 0] = self.field[1, 2] = 1
        self.field[2, 1] = self.field[2, 2] = 1
        self.assertFalse(
            CreatorPath(self.field).has_isolated_empty_cells(
                (2, 2), 1, False))
        self.assertFalse(
            CreatorPath(self.field).has_isolated_empty_cells(
                (2, 2), 2, False))

    def test_can_add_cell(self):
        self.field[0, 0] = self.field[1, 1] = 1
        self.assertTrue(
            CreatorPath(self.field).can_add_cell((1, 0), 1))

        self.field[0, 0] = 1
        self.field[1, 0] = self.field[1, 2] = 1
        self.assertTrue(
            CreatorPath(self.field).can_add_cell((1, 1), 1))
