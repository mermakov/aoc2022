from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, Union

from part import as_computer, Part


@dataclass
class Monkey:
    op: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None
    value: Optional[int] = None


def _read_input(
    lines: Iterator[str],
) -> Iterator[tuple[str, Union[int, tuple[str, str, str]]]]:
    for line in lines:
        key, *args = line.replace(':', '').split(' ')
        if len(args) == 1:
            yield key, int(args[0])
        else:
            yield key, tuple(args)


def _construct_monkeys(lines: Iterator[str]) -> dict[str, Monkey]:
    monkeys = defaultdict(Monkey)

    for key, args in _read_input(lines):
        if isinstance(args, int):
            monkeys[key].value = args
        else:
            left, op, right = args
            monkeys[key].op = op
            monkeys[key].left = left
            monkeys[key].right = right

    return monkeys


def _calculate(monkeys: dict, key: str, raise_for_human: bool = False) -> int:
    if raise_for_human and key == 'humn':
        raise RuntimeError

    monkey = monkeys[key]
    if monkey.value is not None:
        return monkey.value

    op = monkey.op
    left = _calculate(monkeys, monkey.left, raise_for_human=raise_for_human)
    right = _calculate(monkeys, monkey.right, raise_for_human=raise_for_human)

    if op == '+':
        monkey.value = left + right
    elif op == '-':
        monkey.value = left - right
    elif op == '*':
        monkey.value = left * right
    else:
        monkey.value = left // right

    return monkey.value


@as_computer()
def part1(lines: Iterator[str]):
    monkeys = _construct_monkeys(lines)
    return _calculate(monkeys, 'root')


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]):
    monkeys = _construct_monkeys(lines)
    for key, monkey in monkeys.items():
        print(key, monkey)

    subtree = 'root'
    value = None
    while subtree != 'humn':
        left = right = None
        op = monkeys[subtree].op
        new_subtree = None
        try:
            left = _calculate(
                monkeys, monkeys[subtree].left, raise_for_human=True
            )
            new_subtree = monkeys[subtree].right
        except RuntimeError:
            pass
        try:
            right = _calculate(
                monkeys, monkeys[subtree].right, raise_for_human=True
            )
            new_subtree = monkeys[subtree].left
        except RuntimeError:
            pass

        assert left is None or right is None, 'Algo not applicable'
        cur_value = left if left is not None else right
        if value is None:
            value = cur_value
        else:
            if left is None:
                if op == '+':
                    value = value - cur_value
                elif op == '-':
                    value = value + cur_value
                elif op == '*':
                    value = value // cur_value
                else:
                    value = value * cur_value
            else:
                if op == '+':
                    value = value - cur_value
                elif op == '-':
                    value = cur_value - value
                elif op == '*':
                    value = value // cur_value
                else:
                    value = cur_value // value
        subtree = new_subtree

    return value
