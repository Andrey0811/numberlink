from typing import List

from numberlink.const import DEFAULT_FIELD_HEIGHT
from numberlink.core.creator_path import CreatorPath
from numberlink.core.triangle_field import TriangleField


class Generator:
    @staticmethod
    def generate_triangle_field(size: int) -> List[List]:
        field = [[0]]
        for i in range(1, size):
            field.append([0 for _ in range(i * 2 + 1)])

        return field

    @staticmethod
    def generate_field(size: int = 3) -> List[List]:
        size = max(DEFAULT_FIELD_HEIGHT, size)
        field = Generator.generate_triangle_field(size)
        constructor = CreatorPath(TriangleField(field))

        return constructor.create()
