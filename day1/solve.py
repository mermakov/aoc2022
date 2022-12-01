import sys
from pathlib import Path


def _calc(path: Path, top_n: int) -> int:
    current = 0
    top = []

    try:
        with path.open() as f:
            for line in f.readlines():
                line = line.strip()
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
    except (OSError, ValueError) as e:
        print(f'Something went wrong: {e}', file=sys.stderr)
        raise RuntimeError

    return sum(top)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('-n', type=int, default=1)
    opts = parser.parse_args()

    try:
        print(_calc(opts.input, opts.n))
    except RuntimeError:
        exit(1)
