def get_neighbours(path_map, x, y):
    # Варіанти де може знаходитись сусідня вершина
    # (зліва, зверху, зправа, знизу)
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    # Лямбда функція перевірки значень,
    # чи виходять вони за діапазон
    check_neighbour = lambda x, y: True if 0 <= x < 24 and 0 <= y < 16 else False
    # Повертає список координат і ваг можливих сусідніх вершин,
    # якщо виконується вимога лямбда функції check_neighbour
    return [(path_map[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]