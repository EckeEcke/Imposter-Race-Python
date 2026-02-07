import pygame
from constants import FINISH_LINE_X, GAME_WIDTH, GAME_HEIGHT
from text_outline import render_outline

def draw_everything(screen, game_data, font_intro, font_game):
    screen.fill((25,25,25))
    assets = game_data["assets"]
    
    if game_data["state"] == "GAME" or game_data["state"] == "GAME OVER":
        screen.blit(assets["background"], (0, 0))
        screen.blit(assets["goal"], (FINISH_LINE_X, 0))
        pygame.draw.line(screen, (255, 0, 0), (FINISH_LINE_X, 0), (FINISH_LINE_X, GAME_HEIGHT), 5)
        for char in game_data["chars"]:
            char.draw(screen)

        for jid, label in game_data["char_mapping"].items():
            p_idx = int(label[1:]) - 1
            game_data["players"][p_idx].draw_crosshair(screen, assets)

        if game_data["state"] == "GAME OVER":
            overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            overlay.fill((8, 8, 8, 88))
            title = render_outline("GAME OVER!", font_game, (255, 0, 0), (255, 255, 255), 2)
            sub_title = render_outline(f"{game_data['winner']} WINS!", font_game, (255, 0, 0), (255, 255, 255), 2)
            screen.blit(overlay, (0, 0))
            screen.blit(title, title.get_rect(center=(GAME_WIDTH / 2, 300)))
            screen.blit(sub_title, sub_title.get_rect(center=(GAME_WIDTH / 2, 400)))

    elif game_data["state"] == "INTRO":
        num_players = len(game_data["joysticks"])
        title = render_outline("IMPOSTER RACE", font_game, (255, 0, 0), (255, 255, 255), 2)
        status_color = (0, 225, 0) if num_players >= 2 else (150, 150, 150)
        status_text = f"Players ready: {num_players} / 4"
        if num_players < 2:
            status_text += " (Min. 2 required)"
        else:
            status_text += " - PRESS START"
            
        status_surf = font_intro.render(status_text, True, status_color)

        for char in game_data["intro_chars"]:
            char.state = "running"
            char.draw(screen)

        screen.blit(title, title.get_rect(center=(GAME_WIDTH / 2, 300)))
        screen.blit(status_surf, status_surf.get_rect(center=(GAME_WIDTH / 2, 400)))