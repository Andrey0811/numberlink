import sys

from PyQt5.QtWidgets import QApplication

from numberlink.gui.main_windows import MainWindow

import argparse

from numberlink.core.solver import Solver
from numberlink.core.triangle_field import TriangleField
from numberlink.reader import Reader
from numberlink.core import generator


def arg_parser():
    parser = argparse.ArgumentParser(description='Numberlink. '
                                                 'Console Solve or Generate')
    parser.add_argument('-g', '--generate',
                        type=int, nargs=1,
                        help='Generate field triangle numberlink with size. '
                             'Example: -g 4')
    parser.add_argument('-s', '--solve', type=str, nargs=1,
                        help='Solve a given numberlink, '
                             'which exist in numberlink directory. '
                             'Example: -s field1.txt')
    parser.add_argument('-o', '--output', type=str, nargs=1,
                        help='The output file for the generator or for '
                             'the solution must be specified in order '
                             'not to output it to the console. '
                             'Example: -o field2.txt',
                        default='')
    parser.add_argument('-i', '--interface', type=bool,
                        help='Run with gui interface',
                        default=False)
    return parser


def prepare_data_generate(size: int):
    field = TriangleField(generator.Generator.generate_field(size))
    return field


def prepare_data_solve(field: TriangleField) -> str:
    solver = Solver()

    solutions = set(TriangleField(
        solver.get_field_from_solution(field, solution))
        for solution in solver.solve(field))

    if len(solutions) > 0:
        result = f'Count Solutions = {len(solutions)}\n'
        return result + str(solutions.pop())


def read_file(name: str):
    filename = Reader.search_file(name)
    reader = Reader(filename)
    field = TriangleField(reader.get_field_from_file(filename))
    return field


def show_data(data: str, output=''):
    if output == '':
        print(data)
    else:
        try:
            with open(output, 'w+') as f:
                f.write(data)
        except Exception as e:
            print(e)
            print(data)


args = arg_parser().parse_args()
if args.interface:
    if args.output:
        NAME_SAVE_FILE = args.output
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyle('Fusion')
    sys.exit(app.exec())
else:
    if args.generate and args.solve:
        show_data(
            prepare_data_solve(
                prepare_data_generate(args.generate)),
            args.output)
    elif args.solve:
        show_data(
            prepare_data_solve(read_file(args.solve)),
            args.output)
    elif args.generate:
        show_data(
            str(prepare_data_generate(args.generate)),
            args.output)
