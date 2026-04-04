import pygame
from pygame.locals import *
import random
import sys, os

pygame.init()

# ---------- Utilities ----------
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

# ---------- Timing & virtual resolution ----------
clock = pygame.time.Clock()
FPS = 60

VIRTUAL_W = 648
VIRTUAL_H = 702

# virtual drawing surface (game world)
game_surface = pygame.Surface((VIRTUAL_W, VIRTUAL_H))

# real window (resizable)
display_info = pygame.display.Info()
WINDOW_W = display_info.current_w
WINDOW_H = display_info.current_h
window = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)

pygame.display.set_caption("Flappy Bird - Multiplayer")

# ---------- Load images (preload & scale where needed) ----------
bg = pygame.image.load(resource_path("Images/background.png")).convert_alpha()
groundImg = pygame.image.load(resource_path("Images/ground.png")).convert_alpha()
buttonImg = pygame.image.load(resource_path("Images/restart.png")).convert_alpha()
gameOverTextImg = pygame.image.load(resource_path("Images/gameover.png")).convert_alpha()

# cloud sheets (each sheet contains 4 clouds together; we'll treat whole sheet as one sprite)
cloud_imgs = []
for i in range(1, 4):
    img = pygame.image.load(resource_path(f"Images/clouds{i}.png")).convert_alpha()
    
    # downscale clouds sheets a bit for performance & fit (tweak scale factor if needed)
    scale = 0.6
    img = pygame.transform.smoothscale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    cloud_imgs.append(img)

# bird frames scaling
def load_bird_frames(player_id):
    frames = []
    for num in range(1, 4):

        #Load image based on player ID

        #Load image for 1st player
        if player_id == 1:
            img = pygame.image.load(resource_path(f"Images/p1bird{num}.png")).convert_alpha()
            img = pygame.transform.smoothscale(img, (51, 36))  # chosen size; tweak if desired
            frames.append(img)

        #Load image for 2nd player
        elif player_id == 2:
            img = pygame.image.load(resource_path(f"Images/p2bird{num}.png")).convert_alpha()
            img = pygame.transform.smoothscale(img, (51, 36))  # chosen size; tweak if desired
            frames.append(img)

    return frames



pipe_img = pygame.image.load(resource_path("Images/pipe.png")).convert_alpha()

# ---------- Fonts ----------
font = pygame.font.SysFont("Bauhaus 93", 60)
fpsFont = pygame.font.SysFont("Consolas", 20)

# ---------- Colors ----------
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
BLUE = (0, 200, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# ---------- Game variables ----------
drawFPS = True
groundScroll = 0
scrollSpeed = 4
groundImgHeight = VIRTUAL_H - groundImg.get_height()
birdFallSpeed = 8
birdJumpSpeed = 10
pipeGap = 175
pipeFrequency = 1500  # ms
lastPipe = pygame.time.get_ticks() - pipeFrequency
gameOver = False
enableCollision = True

# ----------- FPS tresholds -----------
minFPS = 30
maxFPS = 120


# multiplayer scores
score_p1 = 0
score_p2 = 0

passedPipesGlobal = []  # not used for scoring now, per-bird used instead

enableInput = True
startGame = False
resetCooldown = 0

# clouds (fixed interval)
cloudTimer = pygame.time.get_ticks()
cloudInterval = 2500  # ms
cloud_min_spacing = 350  # horizontal spacing to avoid overlap
LANES = [40, 120, 200]
cloud_cycle_index = 0  # to cycle through cloud images (no random timing)

# bird rotation control
birdRotationController = 1.25

# high score storage
def load_high_score():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
        return 0
    else:
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0

def save_high_score(val):
    with open("highscore.txt", "w") as f:
        f.write(str(int(val)))

high_score = load_high_score()

# ---------- Helper draw functions ----------
def draw_text(surface, text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    surface.blit(img, (x, y))

def draw_text_shadow(surface, text, font_obj, color, x, y, shadow_offset=2):
    shadow = font_obj.render(text, True, BLACK)
    surface.blit(shadow, (x + shadow_offset, y + shadow_offset))
    img = font_obj.render(text, True, color)
    surface.blit(img, (x, y))

# ---------- Reset game logic ----------
def reset_game():
    global score_p1, score_p2, startGame, resetCooldown
    pipeGroup.empty()
    # reset birds
    for bird in birdGroup:
        bird.rect.x = bird.start_x
        bird.rect.centery = int(VIRTUAL_H / 2)
        bird.velocity = 0
        bird.index = 0
        bird.image = bird.frames[0]
        bird.clicked = False
        bird.passed_pipe = False
        bird.alive = True
        bird.flying = False
    score_p1 = 0
    score_p2 = 0
    startGame = False
    resetCooldown = pygame.time.get_ticks() + 300
    return 0

# ---------- Classes ----------
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, control_type, color_tag):
        super().__init__()
        if color_tag == "P1":
            self.frames = load_bird_frames(1)
        elif color_tag == "P2":
            self.frames = load_bird_frames(2)
        self.index = 0
        self.counter = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.start_x = x

        self.velocity = 0
        self.clicked = False
        self.flying = False
        self.control_type = control_type  # "mouse" or "keyboard"
        self.passed_pipe = False
        self.alive = True
        self.color_tag = color_tag  # just an identifier

    def update(self):
        global startGame

        # gravity applied per-bird once it is 'flying'
        if self.flying and self.alive:
            self.velocity += 0.5
            if self.velocity > birdFallSpeed:
                self.velocity = birdFallSpeed
            if self.rect.bottom < groundImgHeight:
                self.rect.y += int(self.velocity)

        # If dead, freeze animation rotation to -90 later handled below
        if not self.alive:
            # freeze animation index
            self.image = pygame.transform.rotate(self.frames[self.index], -90)

            # keep falling due to gravity
            self.velocity += 0.5
            if self.velocity > birdFallSpeed:
                self.velocity = birdFallSpeed
            self.rect.y += int(self.velocity)

            # slight push backward while falling
            self.rect.x -= 2   # adjust speed if needed (2–4 looks best)

            return

        # Input handling (per control type)
        keys = pygame.key.get_pressed()
        mouse_down = pygame.mouse.get_pressed()[0]

        jump_pressed = False
        if self.control_type == "mouse":
            jump_pressed = mouse_down
        elif self.control_type == "keyboard":
            jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP]

        # Jump action: only if bird alive and inputs enabled and cooldown passed
        if jump_pressed and (not self.clicked) and enableInput and pygame.time.get_ticks() > resetCooldown:
            self.clicked = True
            self.velocity = -birdJumpSpeed
            self.flying = True
            startGame = True

        if not jump_pressed:
            self.clicked = False

        # Animation frame handling
        self.counter += 1
        flap_cooldown = 5
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0

        # rotation based on velocity
        self.image = pygame.transform.rotate(self.frames[self.index], self.velocity * -2 / birdRotationController)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pipe_img
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipeGap / 2)]
        else:   
            self.rect.topleft = [x, y + int(pipeGap / 2)]

    def update(self):
        delta = clock.get_time()
        if startGame:
            self.rect.x -= scrollSpeed  
            if self.rect.right < 0:
                self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, target_surface):
        action = False
        pos = pygame.mouse.get_pos()
        # translate pos to virtual surface coords later: here we use window coords,
        # but Button is drawn on virtual surface so mouse pos must be scaled by inverse transform.
        # We'll call this draw after scaling math and handle click detection using scaled mouse coords.
        target_surface.blit(self.image, (self.rect.x, self.rect.y))
        return action  # We'll handle click detection outside where we have scaled mouse coords.

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, lane_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = VIRTUAL_W
        self.rect.y = lane_y
        self.speed = max(1, scrollSpeed // 3)

    def update(self):
        if startGame:
            self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# ---------- Sprite groups ----------
birdGroup = pygame.sprite.Group()
pipeGroup = pygame.sprite.Group()
cloudGroup = pygame.sprite.Group()

# ---------- Create two players ----------
# Player 1: mouse; Player 2: keyboard
player1 = Bird(100, int(VIRTUAL_H / 2), "mouse", "P1")
player2 = Bird(160, int(VIRTUAL_H / 2), "keyboard", "P2")

birdGroup.add(player1)
birdGroup.add(player2)

# ---------- UI objects ----------
button = Button(VIRTUAL_W // 2 - 50, VIRTUAL_H // 2 - 100, buttonImg)
start_text = "Click to Start"
start_text_pos = (VIRTUAL_W // 2, VIRTUAL_H // 2)

# ---------- Cloud spawn helper (no overlap) ----------
def can_spawn_cloud():
    # ensure last cloud is sufficiently left to avoid overlap or there are none
    if len(cloudGroup) == 0:
        return True
    last = cloudGroup.sprites()[-1]
    return last.rect.x < VIRTUAL_W - cloud_min_spacing

def spawn_cloud():
    global cloud_cycle_index
    if not can_spawn_cloud():
        return
    lane = random.choice(LANES)
    img = cloud_imgs[cloud_cycle_index % len(cloud_imgs)]
    cloud = Cloud(img, lane)
    cloudGroup.add(cloud)
    cloud_cycle_index += 1

# ---------- Scoring helper ----------
def handle_scoring():
    global score_p1, score_p2
    if len(pipeGroup) == 0:
        return
    first_pipe = pipeGroup.sprites()[0]
    for bird in birdGroup:
        if not bird.alive:
            continue
        # if bird is in the gap region
        if bird.rect.left > first_pipe.rect.left and bird.rect.right < first_pipe.rect.right and not bird.passed_pipe:
            bird.passed_pipe = True
        # if bird passed the pipe completely -> award score
        if bird.passed_pipe and bird.rect.left > first_pipe.rect.right:
            if bird.control_type == "mouse":
                score_p1 += 1
            else:
                score_p2 += 1
            bird.passed_pipe = False

# ---------- Collision helper ----------
def handle_collisions():
    global gameOver
    alive = 0
    for bird in birdGroup:
        if not bird.alive and enableCollision:
            continue
        # pipe collision
        if pygame.sprite.spritecollide(bird, pipeGroup, False) and enableCollision:
            bird.alive = False
            continue
        # ground/top collision
        if (bird.rect.bottom >= groundImgHeight or bird.rect.top <= 0) and enableCollision:
            bird.alive = False
            continue
        alive += 1
    if alive == 0:
        gameOver = True

# ---------- Ground rendering helper ----------
def draw_ground(surface):
    surface.blit(groundImg, (groundScroll, groundImgHeight))
    surface.blit(groundImg, (groundScroll + groundImg.get_width(), groundImgHeight))

original_button_y = button.rect.y

# ---------- Main loop ----------
run = True
while run:
    dt = clock.tick(FPS)
    # update timers
    timeNow = pygame.time.get_ticks()

    # ====== Input events ======
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            # debug / toggles
            if event.key == pygame.K_F1:
                drawFPS = not drawFPS
            if event.key == pygame.K_F10:
                high_score = 0
                save_high_score(0)
            if event.key == pygame.K_F2:
                enableCollision = not enableCollision
            if event.key == pygame.K_r:
                reset_game()
                gameOver = False
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_F6:    
                FPS -= 10
                if FPS < minFPS:
                    FPS = minFPS
            if event.key == pygame.K_F7:
                FPS += 10
                if FPS > maxFPS:
                    FPS = maxFPS
                


            # let keyboard player start flying on keydown (SPACE/UP)
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                for b in birdGroup:
                    if b.control_type == "keyboard" and b.alive:
                        b.flying = True
                        
                        # also treat as jump press handled in update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # clicking inside virtual coords will be handled later after scaling conversion
            # but allow mouse-controlled bird to start flying (a click)
            for b in birdGroup:
                if b.control_type == "mouse" and b.alive:
                    b.flying = True

    # ====== Game updates & drawing on virtual surface ======
    # clear
    game_surface.blit(bg, (0, 0))

    # --- Clouds ---
    cloudGroup.draw(game_surface)

    # --- Birds ---
    birdGroup.draw(game_surface)
    birdGroup.update()

    # --- Pipes ---
    pipeGroup.draw(game_surface)

    # --- Spawn clouds at fixed interval (no overlap) ---
    if startGame and not gameOver:
        if timeNow - cloudTimer > cloudInterval:
            if can_spawn_cloud():
                spawn_cloud()
                cloudTimer = timeNow
    cloudGroup.update()

    # --- Pipes spawn & movement & scoring & ground movement ---
    if not gameOver and startGame:
        # pipe spawn

        

        if timeNow  - lastPipe > pipeFrequency:
            pipeHeight = random.randint(-100, 100)
            btmPipe = Pipe(VIRTUAL_W, int(VIRTUAL_H / 2) + pipeHeight, -1)
            topPipe = Pipe(VIRTUAL_W, int(VIRTUAL_H / 2) + pipeHeight, 1)
            pipeGroup.add(btmPipe)
            pipeGroup.add(topPipe)
            lastPipe = timeNow

        pipeGroup.update()

        # scoring (per-bird)
        handle_scoring()

        # ground scroll
        groundScroll -= scrollSpeed
        if abs(groundScroll) > groundImg.get_width():
            groundScroll = 0

    # draw ground always
    draw_ground(game_surface)

    # draw UI: scores & best
    draw_text_shadow(game_surface, f"{score_p1}", font, YELLOW, game_surface.get_width()/2 - 50, 10)
    draw_text_shadow(game_surface, f"{score_p2}", font, BLUE, game_surface.get_width()/2 + 50, 10)
    draw_text_shadow(game_surface, f"Best: {high_score}", fpsFont, WHITE, VIRTUAL_W - 140, 10)

    # FPS display
    if drawFPS:
        fps_val = int(clock.get_fps())
        draw_text(game_surface, f"FPS: {fps_val}", fpsFont, WHITE, 10, VIRTUAL_H - 30)
    # start text when not started
    if not startGame:
        draw_text_shadow(game_surface, start_text, font, WHITE, VIRTUAL_W//2 - 150, VIRTUAL_H//2 - 50)

    # collision check (multiplayer)
    handle_collisions()

    # if game over -> update high score
    if gameOver:
        best = max(score_p1, score_p2)

        if best > high_score:
            high_score = best
            save_high_score(high_score)

         #Create total score 
        total_score = (score_p1*2) + score_p2
        total_score_text = f"Total Score: {total_score}"
        
        draw_text_shadow(game_surface, total_score_text, font, GOLD, VIRTUAL_W//2 - 170, VIRTUAL_H//2)
        
        # draw game over text
        scaled_gameOverImg = pygame.transform.smoothscale(gameOverTextImg, (gameOverTextImg.get_width()//3, gameOverTextImg.get_height()//3))
        game_surface.blit(scaled_gameOverImg, (VIRTUAL_W//2 - scaled_gameOverImg.get_width()//2, VIRTUAL_H//2 - 300))


        # draw restart button and handle click with scaled coordinates
        # we'll draw the button on virtual surface, but need mouse in virtual coords to detect click
        button.rect.y = original_button_y + 200   # ← FIX THIS LINE

        game_surface.blit(button.image, button.rect.topleft)

        mx, my = pygame.mouse.get_pos()

        scale_w = window.get_width() / VIRTUAL_W
        scale_h = window.get_height() / VIRTUAL_H
        scale = min(scale_w, scale_h)

        scaled_w = int(VIRTUAL_W * scale)
        scaled_h = int(VIRTUAL_H * scale)

        x_off = (window.get_width() - scaled_w) // 2
        y_off = (window.get_height() - scaled_h) // 2

        # virtual coords
        vx = int((mx - x_off) / scale)
        vy = int((my - y_off) / scale)

        # 4. Check click in virtual coords
        if pygame.mouse.get_pressed()[0] == 1 and enableInput:
            if button.rect.collidepoint(vx, vy):
                reset_game()
                gameOver = False


    # ====== Scale virtual surface to window with aspect ratio preserved ======
    scale_w = window.get_width() / VIRTUAL_W
    scale_h = window.get_height() / VIRTUAL_H
    
    scale = min(scale_w, scale_h)

    scaled_width = int(VIRTUAL_W * scale)
    scaled_height = int(VIRTUAL_H * scale)

    scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_width, scaled_height))

    x_offset = (window.get_width() - scaled_width) // 2
    y_offset = (window.get_height() - scaled_height) // 2

    # fill window background (letterbox bars)
    window.fill((0, 0, 0))
    window.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.update()

pygame.quit()
# ---------- End of file ----------