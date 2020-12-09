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
                             'not to output it to the console. Example: -o field2.txt',
                        default='')
    return parser


def prepare_data_generate(size: int) -> str:
    field = TriangleField(generator.Generator.generate_field(size))
    return str(field)


def prepare_data_solve(name: str) -> str:
    filename = Reader.search_file(name)
    reader = Reader(filename)
    field = TriangleField(reader.get_field_from_file(filename))
    solver = Solver()

    solutions = set(TriangleField(
        solver.get_field_from_solution(field, solution))
        for solution in solver.solve(field))

    if len(solutions) > 0:
        result = f'Count Solutions = {len(solutions)}\n'
        return result + str(solutions.pop())


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


def main():
    args = arg_parser().parse_args()
    if args.generate:
        return show_data(
            prepare_data_generate(args.generate), args.output)

    if args.solve:
        return show_data(
            prepare_data_solve(args.solve), args.output)


if __name__ == '__main__':
    main()
