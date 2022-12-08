from collections.abc import Iterator
from typing import Any

from part import as_computer, Part


def _read_matrix(lines: Iterator[str]) -> tuple[list[int], int, int]:
    n = 0
    matrix = []

    for line in lines:
        if not n:
            n = len(line)
        matrix.extend(int(c) for c in line)

    m = len(matrix) // n

    return matrix, m, n


def _print_matrix(matrix: list[Any], m: int, n: int) -> None:
    for i in range(m):
        print(' '.join(str(v) for v in matrix[i * n:(i + 1) * n]))
    print()


def _calculate_visible(matrix: list[int], m: int, n: int) -> list[bool]:
    visible = [False] * (m * n)

    def _process_line(s_i, s_j, d_i, d_j) -> None:
        cur_max = -1
        while 0 <= s_i < m and 0 <= s_j < n:
            idx = s_i * m + s_j
            val = matrix[idx]
            if val > cur_max:
                visible[idx] = True
                cur_max = val
            s_i += d_i
            s_j += d_j

    for i in range(m):
        _process_line(i, 0, 0, 1)
        _process_line(i, n - 1, 0, -1)
    for j in range(n):
        _process_line(0, j, 1, 0)
        _process_line(m - 1, j, -1, 0)

    return visible


@as_computer()
def part1(lines: Iterator[str]) -> int:
    matrix, m, n = _read_matrix(lines)
    visible = _calculate_visible(matrix, m, n)
    return sum(visible)


def _calculate_scenic(matrix: list[int], m: int, n: int) -> list[int]:
    def _distance(s_i, s_j, d_i, d_j) -> None:
        val = matrix[s_i * n + s_j]
        distance = 0
        while True:
            s_i += d_i
            s_j += d_j
            if s_i < 0 or s_i == m or s_j < 0 or s_j == n:
                break
            distance += 1
            if matrix[s_i * n + s_j] >= val:
                break
        return distance

    scenic = [0] * (m * n)

    for i in range(1, m - 1):
        for j in range(1, n - 1):
            val = 1
            for d_i, d_j in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                val *= _distance(i, j, d_i, d_j)
            scenic[i * n + j] = val

    return scenic


@as_computer(part=Part.TWO)
def part2(lines: Iterator[str]) -> int:
    matrix, m, n = _read_matrix(lines)
    scenic = _calculate_scenic(matrix, m, n)
    return max(scenic)
