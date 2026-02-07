import os
import pygame
import random
from player import Player
from character import Character
from event_handler import event_handler
from game_updater import update_game
from constants import GAME_WIDTH, GAME_HEIGHT, PLAYER_COLORS
from draw import draw_everything
from assets import load_game_data, load_fonts, create_chars

pygame.init()
pygame.joystick.init()
pygame.mixer.init()

base_path = os.path.dirname(os.path.abspath(__file__))

NAME_FONT, CUSTOM_FONT = load_fonts(base_path)

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

loaded_assets = load_game_data(base_path)
loaded_chars = create_chars(base_path)

num_available = len(loaded_chars)
sel = random.sample(range(num_available), 4)

intro_sheets = [
    pygame.image.load(os.path.join(base_path, "assets", "Character 1.png")).convert_alpha(),
    pygame.image.load(os.path.join(base_path, "assets", "Character 2.png")).convert_alpha(),
    pygame.image.load(os.path.join(base_path, "assets", "Character 3.png")).convert_alpha(),
    pygame.image.load(os.path.join(base_path, "assets", "Character 4.png")).convert_alpha(),
    pygame.image.load(os.path.join(base_path, "assets", "Character 5.png")).convert_alpha(),
    pygame.image.load(os.path.join(base_path, "assets", "Character 10.png")).convert_alpha(),
    pygame.image.load(os.path.join(base_path, "assets", "Character 11.png")).convert_alpha(),
]

intro_chars = [
            Character(0, 550, intro_sheets[0], 999),
            Character(-80, 580, intro_sheets[1], 998),
            Character(-10, 610, intro_sheets[2], 997),
            Character(-50, 40, intro_sheets[3], 996),
            Character(-290, 70, intro_sheets[4], 995),
            Character(-360, 120, intro_sheets[5], 994),
            Character(-200, 160, intro_sheets[6], 993)
        ]

def create_new_game_state(loaded_chars, loaded_assets, name_font):
    num_available = len(loaded_chars)
    sel = random.sample(range(num_available), 4)
    return {
        "state": "INTRO",
        "chars": loaded_chars,
        "assets": loaded_assets,
        "joysticks": {},
        "char_mapping": {},
        "winner": "NOBODY",
        "players": [
            Player("P1", PLAYER_COLORS["P1"], "crosshair_blue", sel[0], name_font),
            Player("P2", PLAYER_COLORS["P2"], "crosshair_red", sel[1], name_font),
            Player("P3", PLAYER_COLORS["P3"], "crosshair_green", sel[2], name_font),
            Player("P4", PLAYER_COLORS["P4"], "crosshair_orange", sel[3], name_font)
        ],
        "intro_chars": intro_chars,
    }

game_state = create_new_game_state(loaded_chars, loaded_assets, NAME_FONT)

def reset_game(game_state, loaded_assets, name_font):
    preserved_joysticks = game_state.get("joysticks", {})
    new_chars = create_chars(base_path)
    num_available = len(new_chars)
    sel = random.sample(range(num_available), 4)

    players = [
        Player("P1", PLAYER_COLORS["P1"], "crosshair_blue", sel[0], name_font),
        Player("P2", PLAYER_COLORS["P2"], "crosshair_red", sel[1], name_font),
        Player("P3", PLAYER_COLORS["P3"], "crosshair_green", sel[2], name_font),
        Player("P4", PLAYER_COLORS["P4"], "crosshair_orange", sel[3], name_font)
    ]

    game_state.clear()
    game_state.update({
        "state": "INTRO",
        "chars": new_chars,
        "assets": loaded_assets,
        "joysticks": preserved_joysticks,
        "char_mapping": {},
        "winner": "NOBODY",
        "players": players,
        "intro_chars": intro_chars,
    })

    all_jids = sorted(preserved_joysticks.keys())
    for i, jid in enumerate(all_jids):
        if i < len(players):
            game_state["char_mapping"][jid] = f"P{i+1}"

while True:
    dt = clock.tick(60) / 1000
    if not event_handler(game_state): break
    update_game(game_state, dt, loaded_assets)
    draw_everything(game_surface, game_state, NAME_FONT, CUSTOM_FONT)
    screen.fill((0, 0, 0))

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