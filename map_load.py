def map_load(name):
    map_list = []
    with open('game_core/maps/' + name, 'r') as file:
        for row in file.read().splitlines():
            map_list.append(list(row))

    return map_list