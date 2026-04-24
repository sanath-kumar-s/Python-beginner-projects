import pygame
from constants import *
from utils import get_piece_image

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
        self.panel_rect = pygame.Rect(BOARD_SIZE, 0, WIDTH - BOARD_SIZE, HEIGHT)

    def draw(self, game):
        self.screen.fill(BG_COLOR)
        self._draw_board(game)
        self._draw_panel(game)
        pygame.display.flip()

    def _draw_board(self, game):
        # Draw squares
        for r in range(8):
            for c in range(8):
                color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(self.screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Check for last move highlighting
                if game.board.last_move:
                    start, end = game.board.last_move
                    if (r, c) == start or (r, c) == end:
                        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill(LAST_MOVE_COLOR)
                        self.screen.blit(highlight, (c * SQUARE_SIZE, r * SQUARE_SIZE))

        # Highlights for selection and valid moves
        if game.selected_piece:
            # Highlight selected square
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(HIGHLIGHT_COLOR)
            self.screen.blit(highlight, (game.selected_piece.col * SQUARE_SIZE, game.selected_piece.row * SQUARE_SIZE))
            
            # Highlight valid moves
            for mr, mc in game.valid_moves:
                pygame.draw.circle(self.screen, VALID_MOVE_COLOR, 
                                 (mc * SQUARE_SIZE + SQUARE_SIZE // 2, mr * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

        # Draw pieces
        for r in range(8):
            for c in range(8):
                piece = game.board.get_piece(r, c)
                if piece:
                    img = get_piece_image(piece)
                    if img:
                        self.screen.blit(img, (c * SQUARE_SIZE, r * SQUARE_SIZE))

        # Labels
        cols = "abcdefgh"
        rows = "87654321"
        for i in range(8):
            # Column labels (bottom)
            text = FONT_TINY.render(cols[i], True, (60, 60, 60))
            self.screen.blit(text, (i * SQUARE_SIZE + 5, BOARD_SIZE - 20))
            # Row labels (left)
            text = FONT_TINY.render(rows[i], True, (60, 60, 60))
            self.screen.blit(text, (5, i * SQUARE_SIZE + 5))

    def _draw_panel(self, game):
        pygame.draw.rect(self.screen, PANEL_COLOR, self.panel_rect)
        
        # Turn indicator
        turn_text = "White's Turn" if game.turn == 'w' else "Black's Turn"
        text_surf = FONT_MAIN.render(turn_text, True, TEXT_COLOR)
        self.screen.blit(text_surf, (BOARD_SIZE + 20, 20))
        
        # Status
        if game.status != "Playing":
            status_color = (255, 100, 100) if "mate" in game.status.lower() else ACCENT_COLOR
            status_surf = FONT_MAIN.render(game.status, True, status_color)
            self.screen.blit(status_surf, (BOARD_SIZE + 20, 70))

        # Captured Pieces (Top Row)
        self._draw_captured(game.captured_black, BOARD_SIZE + 20, 150, 'w') # Pieces captured BY white
        self._draw_captured(game.captured_white, BOARD_SIZE + 20, 200, 'b') # Pieces captured BY black

        # Move History
        history_title = FONT_SIDE.render("History:", True, TEXT_COLOR)
        self.screen.blit(history_title, (BOARD_SIZE + 20, 280))
        
        y_off = 320
        # Show last 10 moves
        for i in range(max(0, len(game.move_log) - 16), len(game.move_log), 2):
            move_num = (i // 2) + 1
            w_move = game.move_log[i]
            b_move = game.move_log[i+1] if i+1 < len(game.move_log) else ""
            move_text = FONT_SIDE.render(f"{move_num}. {w_move} {b_move}", True, (180, 180, 180))
            self.screen.blit(move_text, (BOARD_SIZE + 30, y_off))
            y_off += 30

    def _draw_captured(self, pieces, x, y, taker_color):
        # Scale down captured pieces
        size = 30
        for i, piece in enumerate(pieces[:10]): # Limit display
            img = get_piece_image(piece)
            if img:
                scaled = pygame.transform.smoothscale(img, (size, size))
                self.screen.blit(scaled, (x + i * (size + 2), y))
