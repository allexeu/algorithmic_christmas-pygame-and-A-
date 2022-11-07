import pygame

def collision_test(hitbox, tiles_list):
    hit_list = []
    for tile in tiles_list:
        if hitbox.colliderect(tile):
            hit_list.append(tile)

    return hit_list

def move(hitbox, movement, tiles_list):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    hitbox.x += movement[0]
    hit_list = collision_test(hitbox, tiles_list)
    for tile in hit_list:
        if movement[0] > 0:
            hitbox.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            hitbox.left = tile.right
            collision_types['left'] = True

    hitbox.y += movement[1]
    hit_list = collision_test(hitbox, tiles_list)
    for tile in hit_list:
        if movement[1] > 0:
            hitbox.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            hitbox.top = tile.bottom
            collision_types['top'] = True

    return hitbox, collision_types