import argparse
import importlib
import sys
from pathlib import Path

from part import Part, REGISTRY, run_computer


def main():
    root_dir = Path(__file__).parent
    for day in root_dir.glob('day*'):
        try:
            importlib.import_module(day.name, str(day))
        except ImportError as e:
            print(f'Failed to import from {day}: {e}', file=sys.stderr)

    parser = argparse.ArgumentParser(description='AOC2022 runner')
    parser.add_argument('day', choices=REGISTRY.keys())
    parser.add_argument('--part', type=Part, default=Part.ONE)
    parser.add_argument('--test', action='store_true')

    opts = parser.parse_args()

    computer = REGISTRY[opts.day].get(opts.part)
    if computer is None:
        print(f'Unsupported part {opts.part} for {opts.day}', file=sys.stderr)

    input_path = (
        root_dir / opts.day / ('test.txt' if opts.test else 'input.txt')
    )
    if not input_path.exists():
        print(f'{input_path} is missing', file=sys.stderr)

    print(run_computer(input_path, computer))


if __name__ == '__main__':
    main()
