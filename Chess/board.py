from pieces import King, Queen, Rook, Bishop, Knight, Pawn
import copy

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.white_king = None
        self.black_king = None
        self.last_move = None  # (start_pos, end_pos)
        self.en_passant_target = None # Square that can be captured via en passant
        self._initialize_pieces()

    def _initialize_pieces(self):
        # Pawns
        for col in range(8):
            self.grid[6][col] = Pawn('w', 6, col)
            self.grid[1][col] = Pawn('b', 1, col)

        # Rooks
        self.grid[7][0] = Rook('w', 7, 0)
        self.grid[7][7] = Rook('w', 7, 7)
        self.grid[0][0] = Rook('b', 0, 0)
        self.grid[0][7] = Rook('b', 0, 7)

        # Knights
        self.grid[7][1] = Knight('w', 7, 1)
        self.grid[7][6] = Knight('w', 7, 6)
        self.grid[0][1] = Knight('b', 0, 1)
        self.grid[0][6] = Knight('b', 0, 6)

        # Bishops
        self.grid[7][2] = Bishop('w', 7, 2)
        self.grid[7][5] = Bishop('w', 7, 5)
        self.grid[0][2] = Bishop('b', 0, 2)
        self.grid[0][5] = Bishop('b', 0, 5)

        # Queens
        self.grid[7][3] = Queen('w', 7, 3)
        self.grid[0][3] = Queen('b', 0, 3)

        # Kings
        self.white_king = King('w', 7, 4)
        self.black_king = King('b', 0, 4)
        self.grid[7][4] = self.white_king
        self.grid[0][4] = self.black_king

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None

    def move_piece(self, start_pos, end_pos, simulate=False):
        sr, sc = start_pos
        er, ec = end_pos
        piece = self.grid[sr][sc]
        
        if piece is None:
            return False

        captured_piece = self.grid[er][ec]
        
        # En Passant logic
        if isinstance(piece, Pawn) and (er, ec) == self.en_passant_target:
            # Capture the pawn that moved 2 squares
            direction = -1 if piece.color == 'w' else 1
            captured_piece = self.grid[er - direction][ec]
            self.grid[er - direction][ec] = None

        # Execute move
        self.grid[er][ec] = piece
        self.grid[sr][sc] = None
        piece.update_position(er, ec)

        # Castling logic
        if isinstance(piece, King) and abs(sc - ec) == 2:
            # Move the rook
            if ec == 6: # Kingside
                rook = self.grid[er][7]
                self.grid[er][5] = rook
                self.grid[er][7] = None
                rook.update_position(er, 5)
            elif ec == 2: # Queenside
                rook = self.grid[er][0]
                self.grid[er][3] = rook
                self.grid[er][0] = None
                rook.update_position(er, 3)

        if not simulate:
            self.last_move = (start_pos, end_pos)
            # Update En Passant target
            if isinstance(piece, Pawn) and abs(sr - er) == 2:
                self.en_passant_target = ((sr + er) // 2, sc)
            else:
                self.en_passant_target = None

        return captured_piece

    def is_in_check(self, color):
        king = self.white_king if color == 'w' else self.black_king
        king_pos = (king.row, king.col)
        
        opponent_color = 'b' if color == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece and piece.color == opponent_color:
                    if king_pos in piece.get_potential_moves(self.grid):
                        return True
        return False

    def get_valid_moves(self, piece):
        potential_moves = piece.get_potential_moves(self.grid)
        
        # Add special moves: Castling & En Passant
        if isinstance(piece, King):
            potential_moves.extend(self._get_castling_moves(piece))
        elif isinstance(piece, Pawn):
            if self.en_passant_target:
                er, ec = self.en_passant_target
                direction = -1 if piece.color == 'w' else 1
                if piece.row + direction == er and abs(piece.col - ec) == 1:
                    potential_moves.append((er, ec))

        valid_moves = []
        for er, ec in potential_moves:
            # Simulate move
            original_grid = [row[:] for row in self.grid]
            original_white_king_pos = (self.white_king.row, self.white_king.col)
            original_black_king_pos = (self.black_king.row, self.black_king.col)
            
            # Save piece state (has_moved)
            start_pos = (piece.row, piece.col)
            target_piece = self.grid[er][ec]
            has_moved_before = piece.has_moved
            
            # Simple simulation update
            self.grid[er][ec] = piece
            self.grid[start_pos[0]][start_pos[1]] = None
            orig_row, orig_col = piece.row, piece.col
            piece.row, piece.col = er, ec
            
            if not self.is_in_check(piece.color):
                valid_moves.append((er, ec))
                
            # Restore
            self.grid = original_grid
            piece.row, piece.col = orig_row, orig_col
            piece.has_moved = has_moved_before # Not really needed if we use copy but let's be careful

        return valid_moves

    def _get_castling_moves(self, king):
        moves = []
        if king.has_moved or self.is_in_check(king.color):
            return moves

        row = king.row
        # Kingside
        rook = self.grid[row][7]
        if isinstance(rook, Rook) and not rook.has_moved:
            if self.grid[row][5] is None and self.grid[row][6] is None:
                # Check square traversal
                if not self._is_square_attacked(row, 5, king.color) and not self._is_square_attacked(row, 6, king.color):
                    moves.append((row, 6))

        # Queenside
        rook = self.grid[row][0]
        if isinstance(rook, Rook) and not rook.has_moved:
            if self.grid[row][1] is None and self.grid[row][2] is None and self.grid[row][3] is None:
                if not self._is_square_attacked(row, 2, king.color) and not self._is_square_attacked(row, 3, king.color):
                    moves.append((row, 2))
        return moves

    def _is_square_attacked(self, row, col, defender_color):
        attacker_color = 'b' if defender_color == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece and piece.color == attacker_color:
                    if (row, col) in piece.get_potential_moves(self.grid):
                        return True
        return False
