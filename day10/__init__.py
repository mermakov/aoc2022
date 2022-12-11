from collections.abc import Iterator
from dataclasses import dataclass

from part import as_computer, Part


@dataclass
class Cmd:
    change: int = 0
    duration: int = 1


def _parse_input(lines: Iterator[str]) -> Iterator[Cmd]:
    for line in lines:
        cmd, *args = line.split(' ')
        if cmd == 'noop':
            yield Cmd()
        else:
            yield Cmd(change=int(args[0]), duration=2)


@as_computer()
def part1(lines: Iterator[str]) -> int:
    x = 1
    signal_sum = 0
    cycle = 1

    for cmd in _parse_input(lines):
        for _ in range(cmd.duration):
            if (cycle - 20) % 40 == 0:
                signal_sum += cycle * x
            cycle += 1
        x += cmd.change

    return signal_sum


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> None:
    x = 1
    cycle = 1
    row = ''

    for cmd in _parse_input(lines):
        for _ in range(cmd.duration):
            sprite_x = cycle % 40 - 1
            if x - 1 <= sprite_x <= x + 1:
                row += '#'
            else:
                row += '.'
            if cycle % 40 == 0:
                print(row)
                row = ''
            cycle += 1
        x += cmd.change
