import pygame.font

def draw_text(text, font_name, size, color):
    font = pygame.font.Font('game_core/fonts/' + font_name, size)
    return font.render(text, True, color)
