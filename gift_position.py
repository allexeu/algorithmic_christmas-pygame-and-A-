import random

def possible_gift_position(map_list):
    gift_positions = []
    y = 0
    for row in map_list:
        x = 0
        for tile in row:
            if tile == '2':
                gift_positions.append([x * 16, (y-1) * 16])
                # print(x, y-1)
            x += 1
        y += 1

    return random.choice(gift_positions)

