from draw_text import draw_text

def path_map_render(surface, map_list, color1, color2):
    y = 0
    x = 0
    for row_num, row in enumerate(map_list):
        surface.blit(draw_text(str(row_num), 'BULKYPIX.TTF', 6, color1), (x, y))
        y += 16

    y = 0
    for tile_num in range(0, 24):
        surface.blit(draw_text(str(tile_num), 'BULKYPIX.TTF', 6, color1), (x, y))
        x += 16

    y = 4
    for row_weight_num, row_weight in enumerate(map_list):
        x = 6
        for tile_weight_num, tile_weight in enumerate(row_weight):
            surface.blit(draw_text(str(tile_weight), 'BULKYPIX.TTF', 9, color2), (x, y))
            x += 16
        y += 16
