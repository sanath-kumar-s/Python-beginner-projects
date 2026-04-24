import pygame
import os
from constants import SQUARE_SIZE

PIECES = {}
SOUNDS = {}

def load_assets():
    load_images()
    load_sounds()

def load_images():
    pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']
    path = os.path.join('assets', 'images', 'pieces')
    for piece in pieces:
        img = pygame.image.load(os.path.join(path, f"{piece}.png"))
        PIECES[piece] = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))

def get_piece_image(piece_obj):
    if piece_obj is None:
        return None
    key = f"{piece_obj.color}{piece_obj.abbreviation}"
    return PIECES.get(key)

def load_sounds():
    path = os.path.join('assets', 'sounds')
    for snd in ['move', 'capture', 'check', 'mate', 'illegal']:
        try:
            SOUNDS[snd] = pygame.mixer.Sound(os.path.join(path, f"{snd}.wav"))
        except:
            print(f"Could not load sound: {snd}")

def play_sound(event):
    if event in SOUNDS:
        SOUNDS[event].play()
