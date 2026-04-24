import os
from constants import SQUARE_SIZE

class Piece:
    def __init__(self, color, row, col):
        self.color = color  # 'w' or 'b'
        self.row = row
        self.col = col
        self.has_moved = False
        self.abbreviation = "" # 'K', 'Q', etc.
        self.image = None

    def update_position(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True

    def __repr__(self):
        return f"{self.color}{self.abbreviation}"

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.abbreviation = "K"
        
    def get_potential_moves(self, board_state):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board_state[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.abbreviation = "Q"

    def get_potential_moves(self, board_state):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                target = board_state[nr][nc]
                if target is None:
                    moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return moves

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.abbreviation = "R"

    def get_potential_moves(self, board_state):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                target = board_state[nr][nc]
                if target is None:
                    moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return moves

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.abbreviation = "B"

    def get_potential_moves(self, board_state):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                target = board_state[nr][nc]
                if target is None:
                    moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return moves

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.abbreviation = "N"

    def get_potential_moves(self, board_state):
        moves = []
        potential_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in potential_offsets:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board_state[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.abbreviation = "P"

    def get_potential_moves(self, board_state):
        moves = []
        direction = -1 if self.color == 'w' else 1
        
        # Move forward
        nr, nc = self.row + direction, self.col
        if 0 <= nr < 8 and board_state[nr][nc] is None:
            moves.append((nr, nc))
            # Double move
            if not self.has_moved:
                nr2 = nr + direction
                if board_state[nr2][nc] is None:
                    moves.append((nr2, nc))
        
        # Captures
        for dc in [-1, 1]:
            nr, nc = self.row + direction, self.col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board_state[nr][nc]
                if target is not None and target.color != self.color:
                    moves.append((nr, nc))
                    
        return moves
