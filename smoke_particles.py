import random
import pygame

def smoke_particles(location_x, location_y, surface, color):
    smoke_parts = []

    for _ in range(100):
        smoke_parts.append([[location_x, location_y + 16], [random.randint(0, 16), random.randint(0, 16)], random.randint(1, 5)])

    for smoke_part in smoke_parts:
        smoke_part[0][0] += smoke_part[1][0] + 1
        smoke_part[0][1] += smoke_part[1][1] + 1
        smoke_part[2] -= 0.1
        pygame.draw.circle(surface, color, smoke_part[0], smoke_part[2])
        if smoke_part[2] < 0:
            smoke_parts.remove(smoke_part)