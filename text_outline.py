import pygame

offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]

def render_outline(text, font, text_color, outline_color, outline_width=2):
    outline_surf = font.render(text, True, outline_color)
    bg_size = (outline_surf.get_width() + outline_width * 2, 
               outline_surf.get_height() + outline_width * 2)
    full_surf = pygame.Surface(bg_size, pygame.SRCALPHA)
    for dx, dy in offsets:
        full_surf.blit(outline_surf, (outline_width + dx * outline_width, 
                                      outline_width + dy * outline_width))
    main_text = font.render(text, True, text_color)
    full_surf.blit(main_text, (outline_width, outline_width))
    
    return full_surf