from Astar import *
from map_load import map_load

maze = map_load("level1_astar.txt")

i = 0
j = 0
for row in maze:
    for column in row:
        maze[i][j] = int(maze[i][j])
        j += 1
    i += 1
    j = 0

for row in maze:
    print(row)

start = (0, 0)
end = (6, 2)

path = astar(maze, start, end)
print(path)