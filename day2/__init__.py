from collections.abc import Iterator

from part import as_computer, Part


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


@as_computer()
def part1(lines: Iterator[str]) -> int:
    return sum(_LOOKUP[line.replace(' ', '')] for line in lines)


@as_computer(part=Part.TWO)
def part1(lines: Iterator[str]) -> int:
    result = 0

    for line in lines:
        enemy, strategy = line.split(' ')
        change = ord(strategy) - ord('Y')
        action = enemy + chr(ord('X') + (change + ord(enemy) - ord('A')) % 3)
        result += _LOOKUP[action]

    return result
