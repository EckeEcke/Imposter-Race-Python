import pygame

from constants import GAME_WIDTH, GAME_HEIGHT, PLAYER_SPEED
from text_outline import render_outline

class Player:
    def __init__(self, label, color, crosshair, char_idx, font):
        self.label = label
        self.color = color
        self.crosshair_name = crosshair
        self.char_idx = char_idx
        self.font = font
        self.pos = pygame.Vector2(400, 310)
        self.shot_used = False

    def update(self, joy, dt):
        if not joy:
            return
        move = pygame.Vector2(joy.get_axis(0), joy.get_axis(1))
        self.pos += move * PLAYER_SPEED * dt

        self.pos.x = max(0, min(self.pos.x, GAME_WIDTH))
        self.pos.y = max(0, min(self.pos.y, GAME_HEIGHT))

    def shoot(self, chars, assets):
        if self.shot_used:
            return
        self.shot_used = True
        assets["shot_sound"].play()

        shot_rect = pygame.Rect(0, 0, 20, 20)
        shot_rect.center = self.pos

        for c in chars:
            if c.state != "is_dead" and c.hitbox.colliderect(shot_rect):
                c.kill()

    def draw_crosshair(self, surface, assets):
        if self.shot_used:
            return
        img = assets[self.crosshair_name]
        rect = img.get_rect(center=self.pos)
        surface.blit(img, rect)
        txt = render_outline(self.label, self.font,self.color, (255, 255, 255), 2)
        surface.blit(txt, (rect.right + 5, rect.top - 10))

    def get_character(self, chars):
        return chars[self.char_idx]