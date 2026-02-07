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
        self.killed = False

    def update(self, joy, dt):
        if not joy:
            return
        move = pygame.Vector2(joy.get_axis(0), joy.get_axis(1))
        DEADZONE = 0.2
        if move.length() < DEADZONE:
            move = pygame.Vector2(0, 0)
        else:
            pass

        self.pos += move * PLAYER_SPEED * dt

        self.pos.x = max(0, min(self.pos.x, GAME_WIDTH))
        self.pos.y = max(0, min(self.pos.y, GAME_HEIGHT))

    def shoot(self, chars, assets, players):
        if self.shot_used:
            return
        self.shot_used = True
        assets["shot_sound"].play()

        shot_rect = pygame.Rect(0, 0, 20, 20)
        shot_rect.center = self.pos

        for c in chars:
            if c.state != "is_dead" and c.hitbox.colliderect(shot_rect):
                c.kill()    
                if c.is_player:
                    for p in players:
                        if p.label == c.assigned_player:
                            p.killed = True
                            break

    def draw_crosshair(self, surface, assets):
        if self.killed:
            return
        img_crosshair = assets[self.crosshair_name]
        rect = img_crosshair.get_rect(center=self.pos)
        surface.blit(img_crosshair, rect)
        if not self.shot_used:
            img_bullet = assets["bullet"]
            scaled_img_bullet = pygame.transform.scale(img_bullet, (8, 24))
            surface.blit(scaled_img_bullet, (rect.x - scaled_img_bullet.get_width(), rect.centery - scaled_img_bullet.get_height() / 2))
        txt = render_outline(self.label, self.font,self.color, (255, 255, 255), 2)
        surface.blit(txt, (rect.right + 5, rect.top - 10))

    def get_character(self, chars):
        return chars[self.char_idx]