import functools
import itertools
import json
from collections.abc import Iterator
from typing import Union

from part import as_computer, Part


Packet = Union[list, int]


def _read_input(lines: Iterator[str]) -> Iterator[tuple[Packet, Packet]]:
    left = None
    right = None

    for line in lines:
        if not line:
            yield left, right
            left = None
            right = None
            continue

        if left is None:
            left = json.loads(line)
        elif right is None:
            right = json.loads(line)

    if left and right:
        yield left, right


class OkException(Exception):
    pass


class NotOkException(Exception):
    pass


def _compare_impl(left: Packet, right: Packet) -> None:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                raise OkException
            if left > right:
                raise NotOkException
            return
        _compare_impl([left], right)
        return

    if isinstance(right, int):
        _compare_impl(left, [right])
        return

    for left_item, right_item in zip(left, right):
        _compare_impl(left_item, right_item)

    if len(left) < len(right):
        raise OkException
    if len(left) > len(right):
        raise NotOkException


def _compare(left: Packet, right: Packet) -> int:
    try:
        _compare_impl(left, right)
    except NotOkException:
        return -1
    except OkException:
        return 1
    return 0


@as_computer()
def part1(lines: Iterator[str]) -> int:
    return sum(
        i + 1
        for i, (left, right) in enumerate(_read_input(lines))
        if _compare(left, right) >= 0
    )


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    packets = list(itertools.chain.from_iterable(_read_input(lines)))
    packets.extend(([[2]], [[6]]))
    packets = sorted(packets, key=functools.cmp_to_key(_compare), reverse=True)
    result = 1
    for i, packet in enumerate(packets):
        if packet == [[2]] or packet == [[6]]:
            result *= i + 1

    return result
