from pathlib import Path
from typing import List

from app.const import NAME_SAVE_FILE, SEPARATORS


def get_field_from_file(filename: str) -> List[List]:
    result = []
    with open(filename) as f:
        i = f.readline()
        while i != '':
            temp = []
            for j in i:
                if j in SEPARATORS:
                    continue
                else:
                    temp.append(int(j))
            result.append(temp)
            i = f.readline()

    if check_field(result):
        return result


def get_file_from_list(field: List[List], filename: str):
    with open(filename, 'w+') as f:
        output_str = [''.join(map(str, i)) for i in field]
        f.write('\n'.join(map(str, output_str)))


def get_full_path(filename: str) -> str:
    path = go_to_resources()
    return str(path) + path.root + filename


def go_to_resources() -> Path:
    path = Path.cwd()
    return Path(str(str(path) + path.root + 'resources'))


def exist_save_field() -> bool:
    path = go_to_resources()
    path = Path(str(path) + path.root + NAME_SAVE_FILE)
    return path.exists()


def check_field(field: List[List]) -> bool:
    if len(field) <= 2:
        return False

    if len(field[0]) != 1:
        field = reversed(field)

    start = 1
    for i in field[1:]:
        start += 2

        if len(i) != start:
            return False

    return True


def save_list_of_field(field: List[List]):
    get_file_from_list(field, get_full_path(NAME_SAVE_FILE))


def get_field_from_save():
    return get_field_from_file(get_full_path(NAME_SAVE_FILE))
