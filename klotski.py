DIRECTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

class Piece:
    def __init__(self, name, h, w, pos):
        self.name = name
        self.h = h
        self.w = w
        self.pos = pos

    def cells_occupied(self):
        r, c = self.pos
        return {(r + dr, c + dc) for dr in range(self.h) for dc in range(self.w)}

class Position:
    def __init__(self, pieces=None):
        self.pieces = pieces if pieces is not None else []

    @classmethod
    def from_grid(cls, grid):
        cells = {}
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell != ".":
                    cells.setdefault(cell, []).append((r, c))

        pieces = []
        for name, coords in cells.items():
            r0 = min(r for r, _ in coords)
            c0 = min(c for _, c in coords)
            h = max(r for r, _ in coords) - r0 + 1
            w = max(c for _, c in coords) - c0 + 1
            pieces.append(Piece(name, h, w, (r0, c0)))
        return cls(pieces)

    def get_piece(self, name):
        for p in self.pieces:
            if p.name == name:
                return p
        return None

    def make_move(self, move, rows, cols):
        piece_name, direction = move
        piece = self.get_piece(piece_name)
        if piece is None or direction not in DIRECTIONS:
            return None

        dr, dc = DIRECTIONS[direction]
        other_pieces = set().union(*(p.cells_occupied() for p in self.pieces if p is not piece))

        for r, c in piece.cells_occupied():
            new_r, new_c = r + dr, c + dc
            # out of bounds
            if not (0 <= new_r < rows and 0 <= new_c < cols):
                return None
            # already occupied by another piece
            if (new_r, new_c) in other_pieces:
                return None

        new_piece = Piece(piece.name, piece.h, piece.w,(piece.pos[0] + dr, piece.pos[1] + dc))
        new_pieces = [new_piece if p is piece else p for p in self.pieces]
        return Position(new_pieces)

class Klotski:
    def __init__(self, pid, rows, cols, exit_cols, target, grid):
        self.id = pid
        self.rows = rows
        self.cols = cols
        self.target = target
        self.game = [Position.from_grid(grid)]

        t = self.game[0].get_piece(target)
        self.goal_pos = (rows - t.h, min(exit_cols))

    def get_current_pos(self):
        return self.game[-1]

    def get_current_pieces(self):
        return self.get_current_pos().pieces

    def push(self, move):
        new_pos = self.get_current_pos().make_move(move, self.rows, self.cols)
        if new_pos is None:
            return False
        self.game.append(new_pos)
        return True

    def pop(self):
        if len(self.game) > 1:
            self.game.pop()

    def is_win(self):
        return self.get_current_pos().get_piece(self.target).pos == self.goal_pos
