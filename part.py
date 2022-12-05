from collections import defaultdict
from collections.abc import Callable, Iterator
from enum import Enum
from pathlib import Path
from typing import Any


PartComputer = Callable[[Iterator[str]], Any]


class Part(Enum):
    ONE = '1'
    TWO = '2'

    def __str__(self) -> str:
        return self.value


def run_computer(path: Path, computer: PartComputer, strip: bool = True) -> Any:
    with path.open() as f:
        return computer(
            line.strip() if strip else line for line in f.readlines()
        )


REGISTRY = defaultdict(lambda: defaultdict(PartComputer))


def as_computer(part: Part = Part.ONE, **kwargs):
    def deco(f):
        REGISTRY[Path(f.__globals__['__file__']).parent.name][part] = (
            f,
            kwargs,
        )
        return f

    return deco
