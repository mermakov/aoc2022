from collections.abc import Callable, Iterator

from part import as_computer, Part


Assignment = tuple[int, int, int, int]
AssignmentPredicate = Callable[[Assignment], bool]


def _calc(lines: Iterator[str], predicate: AssignmentPredicate) -> int:
    return sum(
        1
        for line in lines
        if predicate(tuple(int(i) for i in line.replace('-', ',').split(',')))
    )


@as_computer()
def part1(lines: Iterator[str]) -> int:
    def _predicate(assignment: Assignment) -> bool:
        s1, e1, s2, e2 = assignment
        return s1 <= s2 <= e2 <= e1 or s2 <= s1 <= e1 <= e2

    return _calc(lines, _predicate)


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    def _predicate(assignment: Assignment) -> bool:
        s1, e1, s2, e2 = assignment
        return s1 <= s2 <= e1 or s2 <= s1 <= e2

    return _calc(lines, _predicate)
