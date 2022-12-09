import math
from collections.abc import Iterator

from part import as_computer, Part


_MOVES = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0),
}

Position = tuple[int, int]


def _read_moves(lines: Iterator[str]) -> Iterator[tuple[Position, int]]:
    for line in lines:
        direction, count = line.split(' ')
        yield _MOVES[direction], int(count)


def _draw_map(head: Position, tail: Position, n: int, seen: set[Position]):
    for i in range(-n, n):
        line = ''
        for j in range(-n, n):
            char = '#' if (j, i) in seen else '.'
            if (j, i) == head:
                if head == tail:
                    char = '*'
                else:
                    char = 'H'
            elif (j, i) == tail:
                char = 't'
            line += char
        print(line)

    print('-' * n)


def _update_tail(head: Position, tail: Position) -> Position:
    dx, dy = tuple(a - b for a, b in zip(head, tail))
    if dx * dx + dy * dy <= 2:
        return tail

    def _abs_ceil(v):
        return (-1 if v < 0 else 1) * math.ceil(abs(v))

    return tuple(a + _abs_ceil(b / 2) for a, b in zip(tail, (dx, dy)))


def _calc(lines: Iterator[str], c: int) -> int:
    head = (0, 0)
    tails = [(0, 0)] * c
    seen = set([tails[-1]])
    for direction, count in _read_moves(lines):
        for _ in range(count):
            head = tuple(a + b for a, b in zip(head, direction))
            tails[0] = _update_tail(head, tails[0])
            for i in range(1, c):
                tails[i] = _update_tail(tails[i - 1], tails[i])
            seen.add(tails[-1])

    return len(seen)


@as_computer()
def part1(lines: Iterator[str]) -> int:
    return _calc(lines, 1)


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    return _calc(lines, 9)
