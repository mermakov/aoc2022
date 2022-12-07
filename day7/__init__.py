from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

from part import as_computer, Part


ROOT_DIR = Path('/')


def _parse(lines: Iterator[str]) -> dict:
    seen = set()
    result = defaultdict(int)
    cur_dir: Optional[Path] = None

    for line in lines:
        if line[0] == '$':
            _, cmd, *args = line.split(' ')
            if cmd == 'cd':
                arg = args[0]
                if arg == '/':
                    cur_dir = ROOT_DIR
                else:
                    cur_dir = (cur_dir / arg).resolve()
        else:
            arg, name = line.split(' ')
            if arg != 'dir':
                size = int(arg)
                path = cur_dir / name
                if path in seen:
                    continue
                seen.add(path)
                path = path.parent
                while path != ROOT_DIR:
                    result[path] += size
                    path = path.parent
                result[path] += size

    return result


MAX_SIZE = 100000


@as_computer()
def part1(lines: Iterator[str]) -> int:
    sizes = _parse(lines)
    return sum(size for size in sizes.values() if size <= MAX_SIZE)


TOTAL_SIZE = 70000000
REQUIRED_SIZE = 30000000


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    sizes = _parse(lines)
    unused = TOTAL_SIZE - sizes[ROOT_DIR]
    to_free = REQUIRED_SIZE - unused

    min_ = TOTAL_SIZE
    for size in sizes.values():
        if to_free <= size < min_:
            min_ = size

    return min_
