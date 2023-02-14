import utils
import argparse
import json


def define_parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--height", help="Matrix height", type=int)
    parser.add_argument("-c", "--width", help="Matrix width", type=int)
    parser.add_argument("-p", "--problem", help="Problem ID", type=str)
    parser.add_argument("-f", "--file", help="Filepath", type=str)
    parser.add_argument("-s", "--seed", help="Seed", type=int)

    return parser.parse_args()


if __name__ == "__main__":
    arguments = define_parse_arguments()
    generator = utils.SpaceGenerator(seed=arguments.seed)

    f = open(arguments.file, "w+")
    with f:
        json.dump(generator.generate_pmatrix(arguments.problem, arguments.height, arguments.width), f)
