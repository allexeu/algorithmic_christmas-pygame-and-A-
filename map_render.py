import pygame

def map_render(surface, map_list, tile_size, tiles_list, tiles_hitboxes, scroll):
    y = 0
    for row in map_list:
        x = 0
        for tile in row:
            if tile == '1':
                surface.blit(tiles_list[int(tile)], (x * tile_size - scroll[0], y * tile_size))
            if tile == '2':
                surface.blit(tiles_list[int(tile)], (x * tile_size - scroll[0], y * tile_size))
            if tile != '0':
                tiles_hitboxes.append(pygame.Rect(x * tile_size - scroll[0], y * tile_size, tile_size, tile_size))
            x += 1
        y += 1