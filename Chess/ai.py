import random
import copy
from constants import PIECE_VALUES

# Piece-Square Tables (simplified)
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty # 'Easy', 'Medium', 'Hard'
        self.depth = 1
        if difficulty == 'Medium': self.depth = 3
        elif difficulty == 'Hard': self.depth = 4

    def get_move(self, game):
        if self.difficulty == 'Easy':
            return self._get_random_move(game)
        
        # Minimax
        best_move = None
        best_value = -float('inf')
        
        legal_moves = self._get_all_legal_moves(game, game.turn)
        if not legal_moves:
            return None
            
        random.shuffle(legal_moves) # Add variety
        
        alpha = -float('inf')
        beta = float('inf')
        
        for move in legal_moves:
            # Simulate
            temp_game = game.clone()
            temp_game.select(*move[0])
            temp_game.move(*move[1])
            
            # Handle simulation promotion
            if temp_game.status == "Promoting":
                temp_game.finalize_promotion('Q')
            
            # Since move switched turn, we evaluate from perspective of player who moved
            val = -self._minimax(temp_game, self.depth - 1, -beta, -alpha)
            
            if val > best_value:
                best_value = val
                best_move = move
            alpha = max(alpha, val)
            
        return best_move

    def _minimax(self, game, depth, alpha, beta):
        if depth == 0 or game.status in ["Checkmate", "Stalemate"]:
            return self._evaluate(game)
        
        legal_moves = self._get_all_legal_moves(game, game.turn)
        best_val = -float('inf')
        
        for move in legal_moves:
            temp_game = game.clone()
            temp_game.select(*move[0])
            temp_game.move(*move[1])
            
            # Handle simulation promotion
            if temp_game.status == "Promoting":
                temp_game.finalize_promotion('Q')
            
            val = -self._minimax(temp_game, depth - 1, -beta, -alpha)
            best_val = max(best_val, val)
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return best_val

    def _evaluate(self, game):
        if game.status == "Checkmate":
            return -100000 # Bad for current turn player
        if game.status == "Stalemate":
            return 0
            
        score = 0
        for r in range(8):
            for c in range(8):
                piece = game.board.get_piece(r, c)
                if piece:
                    val = PIECE_VALUES.get(piece.abbreviation.lower(), 0)
                    # Simple PST bonus
                    pst_bonus = 0
                    if piece.abbreviation == 'P':
                        pst_bonus = PAWN_TABLE[r][c] if piece.color == 'b' else PAWN_TABLE[7-r][c]
                    elif piece.abbreviation == 'N':
                        pst_bonus = KNIGHT_TABLE[r][c] if piece.color == 'b' else KNIGHT_TABLE[7-r][c]
                    
                    if piece.color == game.turn:
                        score += val + pst_bonus
                    else:
                        score -= (val + pst_bonus)
        return score

    def _get_random_move(self, game):
        moves = self._get_all_legal_moves(game, game.turn)
        return random.choice(moves) if moves else None

    def _get_all_legal_moves(self, game, color):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = game.board.get_piece(r, c)
                if piece and piece.color == color:
                    valid = game.board.get_valid_moves(piece)
                    for move in valid:
                        moves.append(((r, c), move))
        return moves
