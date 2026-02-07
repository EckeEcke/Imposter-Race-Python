import os
import pygame
import random
from player import Player
from character import Character
from event_handler import event_handler
from game_updater import update_game
from constants import GAME_WIDTH, GAME_HEIGHT
from draw import draw_everything
from assets import load_game_data, load_fonts, create_chars

# 1. Initialisierung
pygame.init()
pygame.joystick.init()
pygame.mixer.init()

base_path = os.path.dirname(os.path.abspath(__file__))

NAME_FONT, CUSTOM_FONT = load_fonts(base_path)

# Fenster & Zeit
screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()

icon_image = pygame.image.load(os.path.join(base_path, "assets", "icon.png"))
pygame.display.set_icon(icon_image)
pygame.display.set_caption("Imposter Race")

# --- START ---
loaded_assets = load_game_data(base_path)
loaded_chars = create_chars(base_path)

num_available = len(loaded_chars)
sel = random.sample(range(num_available), 4)

def create_new_game_state(loaded_chars, loaded_assets, name_font):
    num_available = len(loaded_chars)
    sel = random.sample(range(num_available), 4)
    return {
        "state": "INTRO",
        "chars": loaded_chars,
        "assets": loaded_assets,
        "joysticks": {},       # Joysticks werden beim Reset beibehalten, später überschreiben
        "char_mapping": {},
        "winner": "NOBODY",
        "players": [
            Player("P1", (0, 0, 255), "crosshair_blue", sel[0], name_font),
            Player("P2", (255, 0, 0), "crosshair_red", sel[1], name_font),
            Player("P3", (0, 255, 0), "crosshair_green", sel[2], name_font),
            Player("P4", (255, 165, 0), "crosshair_orange", sel[3], name_font)
        ]
    }

# Initialer Game State
game_state = create_new_game_state(loaded_chars, loaded_assets, NAME_FONT)

def reset_game(game_state, loaded_assets, name_font):
    preserved_joysticks = game_state.get("joysticks", {})
    new_chars = create_chars(base_path)
    num_available = len(new_chars)
    sel = random.sample(range(num_available), 4)

    players = [
        Player("P1", (0, 0, 255), "crosshair_blue", sel[0], name_font),
        Player("P2", (255, 0, 0), "crosshair_red", sel[1], name_font),
        Player("P3", (0, 255, 0), "crosshair_green", sel[2], name_font),
        Player("P4", (255, 165, 0), "crosshair_orange", sel[3], name_font)
    ]

    game_state.clear()
    game_state.update({
        "state": "INTRO",
        "chars": new_chars,
        "assets": loaded_assets,
        "joysticks": preserved_joysticks,
        "char_mapping": {},
        "winner": "NOBODY",
        "players": players
    })

    # Crosshair-Zuweisung wiederherstellen
    all_jids = sorted(preserved_joysticks.keys())
    for i, jid in enumerate(all_jids):
        if i < len(players):
            game_state["char_mapping"][jid] = f"P{i+1}"

while True:
    dt = clock.tick(60) / 1000
    if not event_handler(game_state): break
    update_game(game_state, dt, loaded_assets)
    draw_everything(game_surface, game_state, NAME_FONT, CUSTOM_FONT)
    screen.fill((0, 0, 0))  # Schwarzer Hintergrund

    scale = min(
        SCREEN_WIDTH / GAME_WIDTH,
        SCREEN_HEIGHT / GAME_HEIGHT
    )

    scaled_w = int(GAME_WIDTH * scale)
    scaled_h = int(GAME_HEIGHT * scale)

    scaled_surface = pygame.transform.smoothscale(
        game_surface,
        (scaled_w, scaled_h)
    )

    offset_x = (SCREEN_WIDTH - scaled_w) // 2
    offset_y = (SCREEN_HEIGHT - scaled_h) // 2

    screen.blit(scaled_surface, (offset_x, offset_y))
    pygame.display.flip()


    if game_state["state"] == "RESET":
        reset_game(game_state, loaded_assets, NAME_FONT)

pygame.quit()