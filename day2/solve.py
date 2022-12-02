import sys
from collections.abc import Callable
from pathlib import Path


_LOOKUP = {
    'AX': 4,
    'AY': 8,
    'AZ': 3,
    'BX': 1,
    'BY': 5,
    'BZ': 9,
    'CX': 7,
    'CY': 2,
    'CZ': 6,
}


def _part1(s: str) -> int:
    return _LOOKUP[s.replace(' ', '')]


def _part2(s: str) -> int:
    enemy, strategy = s.split(' ')
    change = ord(strategy) - ord('Y')
    action = enemy + chr(ord('X') + (change + ord(enemy) - ord('A')) % 3)
    return _LOOKUP[action]


def _calc(path: Path, process: Callable[[str], int]) -> int:
    score = 0

    with path.open() as f:
        for line in f.readlines():
            score += process(line.strip())

    return score


if __name__ == '__main__':
    print(_calc(Path(sys.argv[1]), _part1))
    print(_calc(Path(sys.argv[1]), _part2))
