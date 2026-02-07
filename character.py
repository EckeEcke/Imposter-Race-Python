import pygame
import random
from constants import WALK_SPEED, RUN_SPEED, ANIM_SPEED

class Character:
    def __init__(self, x, y, sheet, char_id):
        self.char_id = char_id
        self.pos = pygame.Vector2(x, y)
        self.state = "idle"  # possible states: "idle", "moving", "running", "is_dead", "taunt"
        self.is_player = False
        self.assigned_player = None
        self.animations = {
            "idle":    self.get_animation_row(sheet, 0, 64, 64, 4),
            "moving":  self.get_animation_row(sheet, 2, 64, 64, 6),
            "running": self.get_animation_row(sheet, 3, 64, 64, 6),
            "is_dead": self.get_animation_row(sheet, 6, 64, 64, 8),
            "taunt":   self.get_animation_row(sheet, 5, 64, 64, 4)
        }
        
        self.current_frame = 0
        self.anim_timer = 0
        self.ai_timer = random.uniform(1.0, 4.0)
        
        # define hitbox
        self.image = self.animations["idle"][0]
        self.hitbox = self.image.get_rect(topleft=(x, y)).inflate(-40, -40)

    def update(self, dt):
        self.anim_timer += dt
        if self.anim_timer >= ANIM_SPEED:
            self.anim_timer = 0
            frames = self.animations[self.state]
            if self.state == "is_dead" and self.current_frame == len(frames) - 1:
                pass
            else:
                self.current_frame = (self.current_frame + 1) % len(frames)
            
            self.image = frames[self.current_frame]
        if self.state == "moving":
            self.pos.x += WALK_SPEED * dt
        elif self.state == "running":
            self.pos.x += RUN_SPEED * dt
        self.hitbox.topleft = (self.pos.x + 20, self.pos.y + 20)

    def update_ai(self, dt):
        if self.is_player or self.state == "is_dead":
            return
        self.ai_timer -= dt
        if self.ai_timer <= 0:
            self.state = random.choice(["idle", "moving"])
            self.ai_timer = random.uniform(0.5, 4.0)

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    def kill(self):
        self.state = "is_dead"
        self.current_frame = 0

    def get_animation_row(self, sheet, row_index, frame_w, frame_h, frame_count):
        frames = []
        for i in range(frame_count):
            rect = pygame.Rect(i * frame_w, row_index * frame_h, frame_w, frame_h)
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(sheet, (0, 0), rect)
            frames.append(image)
        return frames