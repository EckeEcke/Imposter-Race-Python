import os
import pygame
from constants import GAME_HEIGHT
from character import Character

def load_fonts(base_path):
    name_font = pygame.font.Font(os.path.join(base_path, "assets", "font.ttf"), 32)
    custom_font = pygame.font.Font(os.path.join(base_path, "assets", "font.ttf"), 80)
    return name_font, custom_font

def load_game_data(base_path):
    music_path = os.path.join(base_path, "assets", "music.mp3")
    pygame.mixer.music.load(music_path)

    goal_img = pygame.image.load(os.path.join(base_path, "assets", "goal.jpg")).convert_alpha()
    
    goal_aspect_ratio = goal_img.get_width() / goal_img.get_height()
    new_goal_width = int(goal_aspect_ratio * GAME_HEIGHT)

    goal_scaled = pygame.transform.scale(goal_img, (new_goal_width, GAME_HEIGHT))

    assets = {
        "crosshair_blue": pygame.image.load(os.path.join(base_path, "assets", "crosshair_blue.png")).convert_alpha(),
        "crosshair_red": pygame.image.load(os.path.join(base_path, "assets", "crosshair_red.png")).convert_alpha(),
        "crosshair_green": pygame.image.load(os.path.join(base_path, "assets", "crosshair_green.png")).convert_alpha(),
        "crosshair_orange": pygame.image.load(os.path.join(base_path, "assets", "crosshair_orange.png")).convert_alpha(),
        "bullet": pygame.image.load(os.path.join(base_path, "assets", "bullet.png")).convert_alpha(),
        "goal": goal_scaled,
        "background": pygame.image.load(os.path.join(base_path, "assets", "background.png")).convert_alpha(),
        "shot_sound": pygame.mixer.Sound(os.path.join(base_path, "assets", "shot.mp3")),
        "well_done_sound": pygame.mixer.Sound(os.path.join(base_path, "assets", "well_done.ogg")),
        "confirm_sound": pygame.mixer.Sound(os.path.join(base_path, "assets", "confirm.mp3")),

    }

    return assets

def create_chars(base_path):
    chars = []
    for i in range(1, 18):
        try:
            path = os.path.join(base_path, "assets", f"Character {i}.png")
            sheet = pygame.image.load(path).convert_alpha()
            new_char = Character(25, (i-1)*40, sheet, i)
            chars.append(new_char)
        except: 
            print(f"Error loading Char {i}")
    return chars