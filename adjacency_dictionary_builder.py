from get_neighbours import get_neighbours

def adj_dict_builder(path_map):
    # Словник суміжності
    adj_dict = {}
    # Для кожної строки і її координати y
    for y, row in enumerate(path_map):
        # Для кожного стовпця і його координати x
        for x, col in enumerate(row):
            # В словник суміжності для координати кожної вершини заноситься вага
            # і координати сусідніх вершини, для цього викликається функція для
            # перевірки можливих сусідніх вершин get_neihbours
            adj_dict[(x, y)] = adj_dict.get((x, y), []) + get_neighbours(path_map, x, y)

    # Повертання створеного словника суміжності
    return adj_dict