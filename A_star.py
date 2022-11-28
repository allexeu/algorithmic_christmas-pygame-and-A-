from heapq import *

# Еврестична функція для роботи алгоритму (Мангеттенська відстань)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* алгоритм
def A_Star(start, goal, adj_dict):
    print("Робота алгоритму A*")
    print("start: %s | goal: %s" % (start, goal))

    # Мінімальна купа (пріоритетна черга)
    queue = []

    # Додаємо до купи початкову вершину
    heappush(queue, (0, start))

    # Початкова вершина не має вартості
    cost_visited = {start: 0}

    # Словник відвіданих вершин
    visited = {start: None}

    while queue:

        # Видалення з купи елементу з мінімальним пріорітетом і передання
        # значень вартості і координат поточної вершини
        # перший елемент в купі завжди вершина старту
        cur_cost, cur_node = heappop(queue)

        # Якщо поточна вершина співпадає з шуканим значенням
        # зупиняємо роботу алгоритму
        if cur_node == goal:
            # Зупиняємо цикл
            break

        # Знаходження сусідніх вершин поточнї вершини
        neighbours = adj_dict[cur_node]

        # Цикл для проходження по кожній сусідній вершині поточної вершини
        for neighbour in neighbours:

            # Передаємо значення вартості і координат сусідньої вершини
            neigh_cost, neigh_node = neighbour

            # Перераховуємо вартість шляху з поточної вершини до сусідньої
            new_cost = cost_visited[cur_node] + neigh_cost

            # Якщо координати сусідньої вершиини ще не є в словнику вартості вершин
            # або перерахована вартість шляху менша
            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:

                # Розрахуванння пріорітету сусідньої вершини
                # за допомого Мангеттенської відстані
                priority = new_cost + heuristic(neigh_node, goal)

                # Занесення значень пріорітету сусідньої вершини до купи
                heappush(queue, (priority, neigh_node))

                # Оновлення вартості шляху до сусідньої вершини
                cost_visited[neigh_node] = new_cost

                # Сусідня вершина пов'язується з поточною
                visited[neigh_node] = cur_node

    # Повертається словник відвіданих вершин
    print("Відвідані вершини: " + str(visited))
    return visited

