from pathlib import Path
from typing import List

from numberlink_puzzle.const import NAME_SAVE_FILE, SEPARATORS


class Reader:
    def __init__(self, resources: str):
        self.path_to_resources = resources
        root = Path.cwd().root
        if self.path_to_resources[-1] != root:
            self.path_to_resources += root

    @staticmethod
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

        return result

    @staticmethod
    def _get_file_from_list(field: List[List], filename: str):
        with open(filename, 'w+') as f:
            output_str = [''.join(map(str, i)) for i in field]
            f.write('\n'.join(map(str, output_str)))

    @staticmethod
    def search_file(filename) -> str:
        path = Path.cwd()
        result = list(path.glob(filename))

        if len(result) == 0:
            result = list(path.glob(filename))
            result += list(Path(str(path) + path.root +
                                'resources').glob(filename))
            result += list(Path(str(path.parent) + path.root +
                                'resources').glob(filename))

        if len(result) > 0:
            return str(result[0])

    @staticmethod
    def get_resources_path() -> str:
        path = Path.cwd()
        if str(path).endswith('numberlink_puzzle'):
            path = path.parent
        return str(Path(str(str(path) + path.root + 'resources')))

    def exist_save_field(self) -> bool:
        path = Path(self.path_to_resources + NAME_SAVE_FILE)
        return path.exists()

    def save_list_of_field(self, field: List[List]):
        self._get_file_from_list(
            field, self.path_to_resources + NAME_SAVE_FILE)

    def get_field_from_save(self):
        return self.get_field_from_file(
            self.path_to_resources + NAME_SAVE_FILE)
