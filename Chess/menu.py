import pygame
from constants import *

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10) # Border
        
        text_surf = FONT_MAIN.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button(WIDTH//2 - 200, 300, 400, 60, "Local Multiplayer", PANEL_COLOR, (60, 60, 60)),
            Button(WIDTH//2 - 200, 400, 400, 60, "Vs AI (Easy)", PANEL_COLOR, (60, 60, 60)),
            # Button(WIDTH//2 - 200, 480, 400, 60, "Vs AI (Hard)", PANEL_COLOR, (60, 60, 60)),
            Button(WIDTH//2 - 200, 480, 400, 60, "Rules", PANEL_COLOR, (60, 60, 60)),
            Button(WIDTH//2 - 200, 560, 400, 60, "Quit", (100, 30, 30), (150, 50, 50))
        ]
        self.showing_rules = False

    def display(self):
        self.screen.fill(BG_COLOR)
        
        if self.showing_rules:
            self._draw_rules()
            pygame.display.flip()
            return
        
        # Title
        title_surf = pygame.font.SysFont('Segoe UI', 80, bold=True).render("ULTIMATE CHESS", True, ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(title_surf, title_rect)
        
        for btn in self.buttons:
            btn.draw(self.screen)
            
        pygame.display.flip()

    def handle_event(self, event):
        if self.showing_rules:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.showing_rules = False
            return None

        if event.type == pygame.MOUSEMOTION:
            for btn in self.buttons:
                btn.check_hover(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, btn in enumerate(self.buttons):
                    if btn.check_hover(event.pos):
                        if i == 2: # Rules
                            self.showing_rules = True
                            return None
                        return i
        return None

    def _draw_rules(self):
        rules = [
            "CHESS RULES SUMMARY",
            "- Pawn: Moves fwd 1/2 sq. Captures diagonally.",
            "- Rook: Moves in straight lines.",
            "- Knight: Moves in 'L' shape. Can jump pieces.",
            "- Bishop: Moves diagonally.",
            "- Queen: Combines Rook and Bishop.",
            "- King: Moves 1 square. Subject to checkmate.",
            "- Castling: Move King 2 sq towards Rook if neither moved.",
            "",
            "CONTROLS:",
            "- Click to Select then Click to Move.",
            "- 'U' to Undo move.",
            "- 'S' to Save / 'L' to Load.",
            "Click anywhere to return."
        ]
        y = 100
        for line in rules:
            color = ACCENT_COLOR if "CHESS" in line or "CONTROLS" in line else TEXT_COLOR
            surf = FONT_SIDE.render(line, True, color)
            rect = surf.get_rect(center=(WIDTH//2, y))
            self.screen.blit(surf, rect)
            y += 40
