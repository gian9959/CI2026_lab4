import heapq
from collections import deque
from itertools import count

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

            problems[pid] = Klotski(pid, exit_cols, target, grid)

        return problems


def bfs(prob):
    if prob.is_win():
        return prob, 0

    visited = {prob.get_current_pos()}
    queue = deque([prob])
    expanded_nodes = 0

    while queue:
        node = queue.popleft()
        expanded_nodes += 1

        for p in node.get_current_pieces():
            for d in DIRECTIONS:
                move = (p.name, d)
                next_node = node.clone()
                if not next_node.push(move) or next_node.get_current_pos() in visited:
                    continue
                visited.add(next_node.get_current_pos())

                if next_node.is_win():
                    return next_node, expanded_nodes
                queue.append(next_node)

    return None, expanded_nodes

def manhattan_distance(prob):
    t = prob.get_current_pos().get_target_piece()
    r, c = t.pos
    gr, gc = prob.goal_pos
    return abs(gr - r) + abs(gc - c)

def a_star(prob):
    best_pos = {prob.get_current_pos(): 0}
    tie = count()
    heap = [(manhattan_distance(prob), 0, next(tie), prob)]
    expanded_nodes = 0

    while heap:
        _, g, _, node = heapq.heappop(heap)
        g = -g
        if g > best_pos[node.get_current_pos()]:
            continue
        if node.is_win():
            return node, expanded_nodes
        expanded_nodes += 1

        for p in node.get_current_pieces():
            for d in DIRECTIONS:
                move = (p.name, d)
                next_node = node.clone()
                if not next_node.push(move):
                    continue
                pos = next_node.get_current_pos()
                new_g = g + 1
                if new_g < best_pos.get(pos, float("inf")):
                    best_pos[pos] = new_g
                    heapq.heappush(heap, (new_g + manhattan_distance(next_node), -new_g, next(tie), next_node))

    return None, expanded_nodes

probs = load_problems("klotski_problems.txt")
for p in probs.values():
    res, ex = bfs(p)
    lenght = 0
    if res:
        lenght = len(res.game) - 1
    print(f"{p.id} BFS SOLUTION: {lenght} steps, {ex} explored nodes")

print()
for p in probs.values():
    res, ex = a_star(p)
    lenght = 0
    if res:
        lenght = len(res.game) - 1
    print(f"{p.id} A* SOLUTION: {lenght} steps, {ex} explored nodes")
