import itertools
from collections.abc import Iterator

from part import as_computer, Part


def _get_type_priority(type_: str) -> int:
    assert len(type_) == 1
    if 'a' <= type_ <= 'z':
        return ord(type_) - ord('a') + 1
    else:
        return ord(type_) - ord('A') + 27


@as_computer(part=Part.ONE)
def part1(lines: Iterator[str]) -> int:
    result = 0

    for line in lines:
        mid = len(line) // 2
        left, right = line[:mid], line[mid:]
        misplace_item_type = next(iter(set(left) & set(right)))
        result += _get_type_priority(misplace_item_type)

    return result


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    result = 0

    for group in iter(lambda: list(itertools.islice(lines, 3)), []):
        common_item_type = next(
            iter(set.intersection(*[set(item) for item in group]))
        )
        result += _get_type_priority(common_item_type)

    return result
