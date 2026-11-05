from klotski import *

def load_problems(path):
    with open(path, encoding="utf-8") as f:

        lines = f.read().splitlines()
        problems = {}
        i, n = 0, len(lines)
        while i < n:
            line = lines[i].strip()
            i += 1
            if not line or line.startswith("#"):
                continue
            if not line.startswith("problem"):
                raise ValueError(f"Line {i}: expected 'problem <id>', found {line}")

            pid = line.split()[1]
            rows = cols = None
            exit_cols = ()
            target = None
            while i < n:
                h = lines[i].strip()
                i += 1
                if h.startswith("====="):
                    break
                if not h:
                    continue

                parts = h.split()
                if parts[0] == "size":
                    rows, cols = int(parts[1]), int(parts[2])
                elif parts[0] == "exit":
                    if parts[1] != "bottom":
                        raise ValueError(f"Line {i}: expected 'bottom', found {h}")
                    exit_cols = tuple(int(x) for x in parts[2:])
                elif parts[0] == "target":
                    target = parts[1]
                else:
                    raise ValueError(f"Line {i}: expected one of: ['size', 'exit bottom', 'target'], found {h}")

            if rows is None or cols is None or target is None or not exit_cols:
                raise ValueError(f"Problem {pid} has invalid formatting")

            grid = []
            while i < n:
                g = lines[i].strip()
                i += 1
                if g.startswith("====="):
                    break
                if g:
                    grid.append(g.split())

            if len(grid) != rows or any(len(r) != cols for r in grid):
                raise ValueError(f"Grid of problem {pid} has invalid size, should be: {rows}x{cols}")

            problems[pid] = Klotski(pid, rows, cols, exit_cols, target, grid)

        return problems

def manhattan_distance(prob):
    t = prob.get_current_pos().get_piece(prob.target)
    r, c = t.pos
    gr, gc = prob.goal_pos
    return abs(gr - r) + abs(gc - c)

problems = load_problems("klotski_problems.txt")
