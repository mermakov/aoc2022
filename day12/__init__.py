from collections import deque
from collections.abc import Iterator

from part import as_computer, Part


class Map:
    def __init__(self, lines: Iterator[str]):
        self._data: list[list[int]] = []

        for i, line in enumerate(lines):
            row: list[int] = []
            for j, char in enumerate(line):
                if char == 'S':
                    self.start = i, j
                    value = -1
                elif char == 'E':
                    self.end = i, j
                    value = ord('z') - ord('a')
                else:
                    value = ord(char) - ord('a')
                row.append(value)
            self._data.append(row)

        self._m = len(self._data)
        self._n = len(self._data[0])

    def get_neighbors(
        self, coord: tuple[int, int], reverse: bool = False
    ) -> Iterator[tuple[int, int]]:
        i, j = coord
        candidates = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
        for c_i, c_j in candidates:
            if c_i < 0 or c_i >= self._m or c_j < 0 or c_j >= self._n:
                continue
            distance = self._data[c_i][c_j] - self._data[i][j]
            if reverse:
                distance = -distance
            if distance <= 1:
                yield c_i, c_j

    @property
    def area(self) -> int:
        return self._m * self._n

    def at(self, coord: tuple[int, int]) -> int:
        i, j = coord
        return self._data[i][j]


@as_computer()
def part1(lines: Iterator[str]) -> int:
    map_ = Map(lines)

    seen = {map_.start}

    bfs_queue = deque([(map_.start, 0)])
    while bfs_queue:
        tail, depth = bfs_queue.popleft()
        for neighbor in map_.get_neighbors(tail):
            if neighbor in seen:
                continue
            bfs_queue.append((neighbor, depth + 1))
            seen.add(neighbor)
            if neighbor == map_.end:
                return depth + 1


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    map_ = Map(lines)

    seen = {map_.end}

    best_route = map_.area
    bfs_queue = deque([(map_.end, 0)])
    while bfs_queue:
        tail, depth = bfs_queue.popleft()
        for neighbor in map_.get_neighbors(tail, reverse=True):
            if neighbor in seen:
                continue
            seen.add(neighbor)
            if map_.at(neighbor) == 0:
                best_route = min(depth + 1, best_route)
            else:
                bfs_queue.append((neighbor, depth + 1))

    return best_route
