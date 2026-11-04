class Klotski:
    def __init__(self, pid, rows, cols, exit_cols, target, grid):
        self.id = pid
        self.rows = rows
        self.cols = cols
        self.exit_cols = tuple(exit_cols)
        self.target = target
        self.grid = grid