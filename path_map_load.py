def path_map_load(name):
    with open('game_core/path_maps/' + name, 'r') as file:
        map_list = [[int(tile) for tile in row] for row in file.read().splitlines()]

    return map_list