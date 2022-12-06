from collections import deque
from collections.abc import Iterator

from part import as_computer, Part


def _calc(lines: Iterator[str], n: int) -> int:
    line = next(lines)

    latest = deque([], n)
    for i, c in enumerate(line):
        latest.append(c)
        if len(set(latest)) == n:
            return i + 1


@as_computer()
def part1(lines: Iterator[str]) -> int:
    return _calc(lines, 4)


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    return _calc(lines, 14)
