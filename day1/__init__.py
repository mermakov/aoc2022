from collections.abc import Iterator

from part import as_computer, Part


def _calc(lines: Iterator[str], top_n: int) -> int:
    current = 0
    top = []

    for line in lines:
        if not line:
            i = 0
            for v in top:
                if current < v:
                    break
                i += 1
            if i > 0 or len(top) < top_n:
                top.insert(i, current)
                if len(top) > top_n:
                    top.pop(0)
            current = 0
        else:
            current += int(line)

    return sum(top)


@as_computer()
def part1(lines: Iterator[str]) -> int:
    return _calc(lines, 1)


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    return _calc(lines, 3)
