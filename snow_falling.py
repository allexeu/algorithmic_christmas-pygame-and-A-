import pygame
import random

snowflakes = []
for _ in range(80):
    x = random.randrange(-32, 384)
    y = random.randrange(0, 256)
    snowflakes.append([x, y])

def snow_falling(surface, surface_size, color):
    for i in range(len(snowflakes)):
        snowflakes[i][0] += 0.1
        snowflakes[i][1] += 0.5
        if snowflakes[i][1] > surface_size[1]:
            snowflakes[i][1] = random.randrange(-32, -1)
            snowflakes[i][0] = random.randrange(-32, surface_size[0])

        pygame.draw.circle(surface, color, snowflakes[i], 2)