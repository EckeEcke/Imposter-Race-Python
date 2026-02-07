import pygame

def render_outline(text, font, text_col, outline_col, outline_width=2):
    # 1. Den Basis-Text rendern (für die Outline)
    outline_surf = font.render(text, True, outline_col)
    
    # 2. Eine größere Surface erstellen, um den Versatz aufzufangen
    bg_size = (outline_surf.get_width() + outline_width * 2, 
               outline_surf.get_height() + outline_width * 2)
    full_surf = pygame.Surface(bg_size, pygame.SRCALPHA)
    
    # 3. Die Outline in alle 4 (oder 8) Richtungen zeichnen
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
    for dx, dy in offsets:
        # Wir skalieren den Offset mit der gewünschten Dicke
        full_surf.blit(outline_surf, (outline_width + dx * outline_width, 
                                      outline_width + dy * outline_width))
    
    # 4. Den eigentlichen farbigen Text oben drauf rendern
    main_text = font.render(text, True, text_col)
    full_surf.blit(main_text, (outline_width, outline_width))
    
    return full_surf