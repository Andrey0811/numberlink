from typing import List

from app.const import DEFAULT_FIELD_HEIGHT
from app.core.creator_path import CreatorPath
from app.core.triangle_field import TriangleField


def generate_triangle_field(size: int) -> List[List]:
    field = [[0]]
    for i in range(1, size):
        field.append([0 for _ in range(i * 2 + 1)])

    return field


def generate_field(size: int = 3):
    size = max(DEFAULT_FIELD_HEIGHT, size)
    field = generate_triangle_field(size)
    constructor = CreatorPath(TriangleField(field))

    return constructor.create()
