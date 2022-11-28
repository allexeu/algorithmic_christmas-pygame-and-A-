# Функція для побудови шляху з відвіданих А* алгоритмом точок
def path_builder(goal, visited):
    # Список вершин шляху
    path = []
    # Додаємо кінцеву вершину в список шляху
    path.append(goal)
    # Призначаємо сегменту шляху значення кінцевої вершини
    path_segment = goal
    # Поки сегмент шляху є в відвіданих точках
    while path_segment in visited:
        # Призначаємо сегменту шляху наступну зв'язану вершину
        path_segment = visited[path_segment]
        # Поки не доходимо до початку словника відвіданих вершин
        if path_segment is not None:
            # Додаємо сегменти шляху
            path.append(path_segment)

    # Повертаємо оброблений шлях
    print("Найкоротший шлях: " + str(path))
    return path
