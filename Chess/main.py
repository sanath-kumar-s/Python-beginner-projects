import pygame
import sys
from constants import *
from game import Game
from gui import GUI
from menu import Menu
from ai import AI
from utils import load_assets, play_sound

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ultimate Python Chess")
    clock = pygame.time.Clock()
    
    # Load assets
    load_assets()
    
    menu = Menu(screen)
    gui = GUI(screen)
    game = None
    ai_player = None
    
    state = "MENU" # MENU, PLAYING, GAME_OVER

    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if state == "MENU":
                choice = menu.handle_event(event)
                if choice is not None:
                    game = Game()
                    if choice == 0: # Multiplayer
                        ai_player = None
                    elif choice == 1: # Easy AI
                        ai_player = AI('Easy')
                    elif choice == 2: # Hard AI
                        ai_player = AI('Hard')
                    elif choice == 3: # Quit
                        pygame.quit()
                        sys.exit()
                    state = "PLAYING"

            elif state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u: # Undo
                        game.undo()
                    if event.key == pygame.K_s: # Save
                        game.save_game()
                    if event.key == pygame.K_l: # Load
                        loaded = Game.load_game()
                        if loaded: game = loaded
                    if event.key == pygame.K_ESCAPE:
                        state = "MENU"
                
                if game.status == "Promoting":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q: game.finalize_promotion('Q')
                        elif event.key == pygame.K_r: game.finalize_promotion('R')
                        elif event.key == pygame.K_b: game.finalize_promotion('B')
                        elif event.key == pygame.K_n: game.finalize_promotion('N')
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Restrict moves if it's AI turn
                    if ai_player and game.turn == 'b':
                        continue

                    if event.button == 1:
                        col = pos[0] // SQUARE_SIZE
                        row = pos[1] // SQUARE_SIZE
                        
                        if row < 8 and col < 8:
                            if game.selected_piece:
                                if game.move(row, col):
                                    play_sound(game.sound_event)
                                else:
                                    play_sound('illegal')
                                    # Try to select new piece
                                    game.select(row, col)
                            else:
                                if not game.select(row, col):
                                    play_sound('illegal')

        # AI Turn Handling
        if state == "PLAYING" and ai_player and game.turn == 'b' and game.status in ["Playing", "Check"]:
            # Show "Thinking" status
            gui.draw(game)
            thinking_text = FONT_MAIN.render("AI is Thinking...", True, (255, 255, 0))
            screen.blit(thinking_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            
            # Delay for Easy mode
            if ai_player.difficulty == 'Easy':
                pygame.time.delay(600)

            # Get AI Move
            move = ai_player.get_move(game)
            if move:
                start, end = move
                game.select(*start)
                game.move(*end)
                play_sound(game.sound_event)
                
                # Check for AI promotion
                if game.status == "Promoting":
                    game.finalize_promotion('Q')
                    play_sound(game.sound_event)
            
            if game.status in ["Checkmate", "Stalemate"]:
                pass # Handled by status draw

        # Draw
        if state == "MENU":
            menu.display()
        elif state == "PLAYING":
            gui.draw(game)
            if game.status == "Promoting":
                # Promotion overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                promo_text = FONT_MAIN.render("Promote Pawn: Q, R, B, N", True, (255, 255, 255))
                screen.blit(promo_text, (WIDTH // 2 - 150, HEIGHT // 2))

            if game.status in ["Checkmate", "Stalemate"]:
                # Draw overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                msg = f"GAME OVER: {game.status}"
                res_surf = FONT_MAIN.render(msg, True, (255, 255, 255))
                res_rect = res_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
                screen.blit(res_surf, res_rect)
                
                hint_surf = FONT_SIDE.render("Press ESC for Main Menu", True, (200, 200, 200))
                hint_rect = hint_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
                screen.blit(hint_surf, hint_rect)
                pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
