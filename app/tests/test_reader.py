import unittest

from app import reader


class ReaderTest(unittest.TestCase):
    @staticmethod
    def test_get_field_from_file():
        actual = reader.get_field_from_file(
                reader.get_full_path('MyField2.txt'))
        expected = [[1], [1, 0, 2], [3, 0, 3, 0, 2]]
        assert len(expected) == len(actual)
        for i in range(len(expected)):
            assert len(expected[i]) == len(actual[i])
            for j in range(len(expected[i])):
                assert expected[i][j] == actual[i][j]