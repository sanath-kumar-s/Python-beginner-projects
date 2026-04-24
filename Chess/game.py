from board import Board
from pieces import Queen, Rook, Bishop, Knight
import copy
import pickle
import os

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.history = []
        self.captured_white = []
        self.captured_black = []
        self.status = "Playing" # "Check", "Checkmate", "Stalemate", "Draw"
        self.selected_piece = None
        self.valid_moves = []
        self.move_log = [] # Algebraic notation
        self.sound_event = None # 'move', 'capture', 'check', 'mate'
        self.promotion_pos = None # (row, col)

    def clone(self):
        """Create a lightweight copy for AI simulation."""
        new_game = Game()
        new_game.board = copy.deepcopy(self.board)
        new_game.turn = self.turn
        new_game.status = self.status
        new_game.captured_white = self.captured_white[:]
        new_game.captured_black = self.captured_black[:]
        return new_game

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def move(self, row, col):
        self.sound_event = None
        if self.selected_piece and (row, col) in self.valid_moves:
            # Save state for undo
            self.history.append(copy.deepcopy(self.board))
            
            start_pos = (self.selected_piece.row, self.selected_piece.col)
            captured = self.board.move_piece(start_pos, (row, col))
            
            if captured:
                self.sound_event = 'capture'
                if captured.color == 'w':
                    self.captured_white.append(captured)
                else:
                    self.captured_black.append(captured)
            else:
                self.sound_event = 'move'

            # Promotion check
            if self._is_promotion(self.selected_piece):
                self.promotion_pos = (row, col)
                self.status = "Promoting"
            else:
                self._finalize_move(start_pos, (row, col), captured)
            
            self.selected_piece = None
            self.valid_moves = []
            return True
        
        self.selected_piece = None
        self.valid_moves = []
        return False

    def finalize_promotion(self, piece_type):
        if self.status == "Promoting" and self.promotion_pos:
            r, c = self.promotion_pos
            color = 'w' if self.turn == 'w' else 'b' # Wait, the turn is still current player's
            if piece_type == 'Q': new_piece = Queen(color, r, c)
            elif piece_type == 'R': new_piece = Rook(color, r, c)
            elif piece_type == 'B': new_piece = Bishop(color, r, c)
            elif piece_type == 'N': new_piece = Knight(color, r, c)
            
            self.board.grid[r][c] = new_piece
            self.promotion_pos = None
            # Now finalize
            self._finalize_move(None, (r, c), None) # Notation might be tricky here

    def _is_promotion(self, piece):
        if piece.abbreviation == 'P':
            if (piece.color == 'w' and piece.row == 0) or (piece.color == 'b' and piece.row == 7):
                return True
        return False

    def _finalize_move(self, start_pos, end_pos, captured):
        # Update move log if not called from promotion
        if start_pos:
            # Re-get the piece from the new position
            piece = self.board.grid[end_pos[0]][end_pos[1]]
            move_str = self._get_algebraic_notation(piece, start_pos, end_pos, captured)
            self.move_log.append(move_str)

        # Switch turn
        self.turn = 'b' if self.turn == 'w' else 'w'
        self._update_status()

    def save_game(self, filename="savegame.dat"):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_game(filename="savegame.dat"):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        return None

    def undo(self):
        if self.history:
            self.board = self.history.pop()
            self.turn = 'b' if self.turn == 'w' else 'w'
            self._update_status()
            self.move_log.pop()
            return True
        return False

    def _check_promotion(self, piece):
        # Auto-promote to Queen for now, GUI can be added later
        if piece.abbreviation == 'P':
            if (piece.color == 'w' and piece.row == 0) or (piece.color == 'b' and piece.row == 7):
                self.board.grid[piece.row][piece.col] = Queen(piece.color, piece.row, piece.col)

    def _update_status(self):
        in_check = self.board.is_in_check(self.turn)
        has_legal_moves = False
        
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece and piece.color == self.turn:
                    if self.board.get_valid_moves(piece):
                        has_legal_moves = True
                        break
            if has_legal_moves:
                break
        
        if not has_legal_moves:
            if in_check:
                self.status = "Checkmate"
                self.sound_event = 'mate'
            else:
                self.status = "Stalemate"
        elif in_check:
            self.status = "Check"
            self.sound_event = 'check'
        else:
            self.status = "Playing"

    def _get_algebraic_notation(self, piece, start, end, captured):
        cols = "abcdefgh"
        rows = "87654321"
        p_type = "" if piece.abbreviation == 'P' else piece.abbreviation
        cap_str = "x" if captured else ""
        end_str = f"{cols[end[1]]}{rows[end[0]]}"
        return f"{p_type}{cap_str}{end_str}"
