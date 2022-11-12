# General imports
import random
from heapq import *
# Pygmae import
import pygame
pygame.init()

# Clock init
clock = pygame.time.Clock()

# Class imports
from GiftObj import GiftObj

# Functions imports
from draw_text import draw_text
from map_load import map_load
from path_map_load import path_map_load
from map_render import map_render
from snow_falling import snow_falling
from collision_test_move import move
from anim_load import anim_load
from change_action import change_action
from gift_position import possible_gift_position

# Main colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
sky_blue = (146, 244, 255)
light_green = (90, 233, 159)

# Sprites load
santa_icon = pygame.image.load('game_core/sprites/santa/santa.png')

# Window settings
window_size = [384 * 3, 256 * 3]
pygame.display.set_icon(santa_icon)
pygame.display.set_caption('Algorithmic Christmas')
screen = pygame.display.set_mode((window_size[0], window_size[1]))

# Surface settings
surface_size = [384, 256]
surface = pygame.Surface((surface_size[0], surface_size[1]))

def main_menu():
    # Buttons list
    buttons = [pygame.Rect(surface_size[0] / 4 + 24, surface_size[1] / 4 + 24, 150, 30),
               pygame.Rect(surface_size[0] / 4 + 24, surface_size[1] / 4 + 24 * 3, 150, 30),
               pygame.Rect(surface_size[0] / 4 + 24, surface_size[1] / 4 + 24 * 5, 150, 30)]

    # Variables for choosing options and menu
    choose_state = 3
    choose_option = {3:'Play', 2:'Options', 1:'Exit'}
    is_chose = False
    choose_mark_pos = [surface_size[0] / 4, surface_size[1] / 4 + 28]

    while True:
        # Screen filling
        surface.fill(sky_blue)

        # Snow falling
        snow_falling(surface, surface_size, white)

        # Logo
        surface.blit(draw_text('Algorithmic', 'BULKYPIX.TTF', 25, white), (surface_size[0] / 4, surface_size[1] / 12))
        surface.blit(draw_text('Christmas', 'BULKYPIX.TTF', 25, red), (surface_size[0] / 4, surface_size[1] / 6))
        surface.blit(santa_icon, (surface_size[0] - 110, surface_size[1] - 210))

        # Buttons
        pygame.draw.rect(surface, white, buttons[0])
        surface.blit(draw_text('Play', 'BULKYPIX.TTF', 25, black), (surface_size[0] / 2 - 32, surface_size[1] / 4 + 28))
        pygame.draw.rect(surface, white, buttons[1])
        surface.blit(draw_text('Options', 'BULKYPIX.TTF', 25, black), (surface_size[0] / 2 - 60, surface_size[1] / 4 + 25 * 3))
        pygame.draw.rect(surface, white, buttons[2])
        surface.blit(draw_text('Exit', 'BULKYPIX.TTF', 25, black), (surface_size[0] / 2 - 26, surface_size[1] / 4 + 25 * 5))

        # Choosing option navigation
        if choose_state > 3:
            choose_state = 1
        if choose_state == 3:
            surface.blit(draw_text('>', 'BULKYPIX.TTF', 25, white), (choose_mark_pos[0], choose_mark_pos[1]))
        if choose_state == 2:
            surface.blit(draw_text('>', 'BULKYPIX.TTF', 25, white), (choose_mark_pos[0], choose_mark_pos[1] + 48))
        if choose_state == 1:
            surface.blit(draw_text('>', 'BULKYPIX.TTF', 25, white), (choose_mark_pos[0], choose_mark_pos[1] + 48 * 2))
        if choose_state < 1:
            choose_state = 3

        # Chose option check
        if is_chose == True:
            if choose_option[choose_state] == 'Play':
                level_1()
            if choose_option[choose_state] == 'Options':
                options()
            if choose_option[choose_state] == 'Exit':
                quit()

        # Event loop
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    choose_state += 1
                if event.key == pygame.K_DOWN:
                    choose_state -= 1

                if event.key == pygame.K_SPACE:
                    is_chose = True

                if event.key == pygame.K_ESCAPE:
                    quit()

            if event.type == pygame.QUIT:
                quit()

        screen.blit(pygame.transform.scale(surface, (window_size[0], window_size[1])), (0, 0))
        pygame.display.update()
        clock.tick(60)

# Level 1
def level_1():
    # Size of tile
    tile_size = 16

    # List of tiles for level
    # 0 - means empty tile
    map_tiles_list = [0, pygame.image.load('game_core/sprites/map/dirt.png'),
                         pygame.image.load('game_core/sprites/map/snow.png'),
                         pygame.image.load('game_core/sprites/map/icy_snow.png'),
                         pygame.image.load('game_core/sprites/map/bricks.png')]

    # Map loading
    map_list = map_load('level3.txt')

    # Gifts tiles
    gifts = [pygame.image.load("game_core/sprites/map/gift.png"),
             pygame.image.load("game_core/sprites/map/gift1.png")]

    # Player tile
    santa = pygame.image.load("game_core/sprites/santa/santa.png")

    # Player hitbox
    santa_hitbox = pygame.Rect(112, 48, tile_size, tile_size)

    # Robot hitbox
    robot_x = 15
    robot_y = 4
    robot_hitbox = pygame.Rect(15 * 16, 4 * 16, tile_size, tile_size)

    # Player movement
    moving_right = False
    moving_left = False
    player_jump = 0
    air_timer = 0

    # Scroll
    true_scroll = [0, 0]

    # Background objects
    background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

    # Flip
    player_flip = False

    # Animation database
    # for loading animations of the whole level
    anim_names_database = {}
    anim_sprites_database = {}

    # Player idle animation
    anim_names_database['idle'] = anim_load(anim_sprites_database, 'santa', 'idle', [45, 45])
    # Player run animation
    anim_names_database['run'] = anim_load(anim_sprites_database, 'santa', 'run', [15, 15])
    # Player jump animation
    anim_names_database['jump'] = anim_load(anim_sprites_database, 'santa', 'jump', [15])

    # For animations work
    player_frame = 0
    player_action = 'idle'

    # Music and sounds
    player_jump_sound = pygame.mixer.Sound('game_core/sounds/santa/jump.wav')
    walking_sounds = [pygame.mixer.Sound('game_core/sounds/map/grass_0.wav'),
                      pygame.mixer.Sound('game_core/sounds/map/grass_1.wav')]
    coin_sound = pygame.mixer.Sound('game_core/sounds/map/coin.wav')

    # Volume setting
    player_jump_sound.set_volume(0.1)
    walking_sounds[0].set_volume(0.1)
    walking_sounds[1].set_volume(0.1)
    coin_sound.set_volume(0.1)

    # Walking sound timer
    walking_timer = 0

    # Gift init
    gift_pos = possible_gift_position(map_list)
    gift_obj = GiftObj(random.choice(gifts), gift_pos)

    # Score
    score_counter = 0

    # A star
    # A* star algorithm realization
    # Get neighbours
    cols, rows = 24, 16
    path_map = path_map_load('level3_path_map.txt')

    def get_circle(x, y):
        return (x * 16 + 16 // 2, y * 16 + 16 // 2), 16 // 4

    def get_neighbours(x, y):
        check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(path_map[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]

    # Heuristic for path cost calculation
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # A*
    def Astar(start, goal, graph):
        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while queue:
            cur_cost, cur_node = heappop(queue)
            if cur_node == goal:
                break

            neighbours = graph[cur_node]
            for neighbour in neighbours:
                neigh_cost, neigh_node = neighbour
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + heuristic(neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node

        return visited

    # Adjency dictionary
    graph = {}
    for y, row in enumerate(path_map):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

    start = (15, 4)
    goal = (gift_pos[0] / 16, gift_pos[1] / 16)
    queue = []
    heappush(queue, (0, start))
    visited = Astar(start, goal, graph)
    print(visited)

    # Robot path
    robot_path = []

    path_head = goal
    # Robot movement
    robot_movement = []
    currentTick = 0



    while True:
        currentTick += 1
        print("======= Game tick ========")
        # Screen filling
        surface.fill(sky_blue)

        # Scroll
        true_scroll[0] = 0
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])

        # Scroll x limiting
        if scroll[0] < 0:
            scroll[0] = 0

        # Backgorund objects
        pygame.draw.rect(surface, (7, 80, 75), pygame.Rect(0, 150, 300, 80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                                   background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                                   background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(surface, (14, 222, 150), obj_rect)
            else:
                pygame.draw.rect(surface, (9, 91, 85), obj_rect)

        # Snow falling
        snow_falling(surface, surface_size, white)

        # Map rendering and hitboxes handling
        tiles_hitboxes = []
        map_render(surface, map_list, tile_size, map_tiles_list, tiles_hitboxes, scroll)

        # Player moving handling
        player_position = [0, 0]
        if moving_right:
            player_position[0] += 3
        if moving_left:
            player_position[0] -= 3

        # Gravity applying
        player_position[1] += player_jump
        player_jump += 0.5
        if player_jump > 8:
            player_jump = 8

        # Collisions
        santa_hitbox, collisions = move(santa_hitbox, player_position, tiles_hitboxes)

        # Sounds handling
        if walking_timer > 0:
            walking_timer -= 1

        # Jumping collisions
        if collisions['bottom']:
            player_jump = 0
            air_timer = 0
            if player_position[0] != 0:
                if walking_timer == 0:
                    walking_timer = 30
                    random.choice(walking_sounds).play()
        else:
            air_timer += 1

        if collisions['top']:
            player_jump = 0

        # Animations and flip handling
        if player_position[0] == 0:
            player_action, player_frame = change_action(player_action, player_frame, 'idle')
        if player_position[0] > 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            player_flip = False
        if player_position[0] < 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            player_flip = True
        if player_position[1] < 0:
            player_action, player_frame = change_action(player_action, player_frame, 'jump')

        # Player frames animation incrementing
        player_frame += 1
        if player_frame >= len(anim_names_database[player_action]):
            player_frame = 0

        # Current player sprite
        santa = anim_sprites_database[anim_names_database[player_action][player_frame]]

        # Player rendering
        surface.blit(pygame.transform.flip(santa, player_flip, False), (santa_hitbox.x, santa_hitbox.y))

        # Collision with gift handling
        if gift_obj.hitbox_collision(santa_hitbox, scroll) or robot_hitbox.colliderect(gift_obj.get_hitbox(scroll)):
            if (len(robot_movement) > 0 and robot_hitbox.x % 16 != 0 and gift_obj.hitbox_collision(santa_hitbox, scroll)):
                bot_move = robot_movement[0]
                print(bot_move)
                if bot_move == 'top':
                    robot_hitbox.y -= 8
                if bot_move == 'right':
                    robot_hitbox.x += 8
                if bot_move == 'left':
                    robot_hitbox.x -= 8
                if bot_move == 'down':
                    robot_hitbox.y += 8
                robot_movement.pop(0)

                surface.blit(santa_icon, (robot_hitbox.x, robot_hitbox.y))

            robot_movement.clear()

            coin_sound.play()
            score_counter += 1
            gift_pos = possible_gift_position(map_list)
            gift_obj = GiftObj(random.choice(gifts), gift_pos)
            goal = (gift_pos[0] / 16, gift_pos[1] / 16)

            if (robot_hitbox.colliderect(gift_obj.get_hitbox(scroll))):
                robot_hitbox.x = goal[0]
                robot_hitbox.y = goal[1]
            start = (int(robot_hitbox.x / 16), int(robot_hitbox.y / 16))
            visited = Astar(start, goal, graph)

            path_head, path_segment = goal, goal
            while path_segment and path_segment in visited:
                path_segment = visited[path_segment]
                if path_segment is not None:
                    robot_path.append(path_segment)

            for index, path in enumerate(robot_path[::-1]):
                if path[0] == robot_path[(len(robot_path) - index - 1) - 1][0]:
                    if path[1] < robot_path[(len(robot_path) - index - 1) - 1][1]:
                        robot_movement.append("down")
                        robot_movement.append("down")
                    if path[1] > robot_path[(len(robot_path) - index - 1) - 1][1]:
                        robot_movement.append("top")
                        robot_movement.append("top")
                else:
                    if path[0] < robot_path[(len(robot_path) - index - 1) - 1][0]:
                        robot_movement.append("right")
                        robot_movement.append("right")
                    elif path[0] > robot_path[(len(robot_path) - index - 1) - 1][0]:
                        robot_movement.append("left")
                        robot_movement.append("left")

            robot_movement.pop(-1)
            robot_movement.pop(-1)
            robot_movement.append(robot_movement[-1])
            robot_movement.append(robot_movement[-1])
        for path in robot_path:
            pygame.draw.circle(surface, pygame.Color('blue'), *get_circle(*path))

        print(robot_movement)
        # for bot_move in robot_movement:
        #     if bot_move == 'top':
        #         robot_hitbox.y -= 1
        #     if bot_move == 'right':
        #         robot_hitbox.x += 1
        #     if bot_move == 'left':
        #         robot_hitbox.x -= 1
        #     if bot_move == 'down':
        #         robot_hitbox.y += 1


# robot movement engine
            # for bot_move in robot_movement:
               # if bot_move == 'top':
                   # robot_hitbox.y -= 1
               # if bot_move == 'right':
                   # robot_hitbox.x += 1
                # if bot_move == 'left':
                   # robot_hitbox.x -= 1
                # if bot_move == 'down':
                   # robot_hitbox.y += 1
                   # break

        if(len(robot_movement) > 0 and currentTick % 5 == 0):
            bot_move = robot_movement[0]
            print(bot_move)
            if bot_move == 'top':
               robot_hitbox.y -= 8
            if bot_move == 'right':
               robot_hitbox.x += 8
            if bot_move == 'left':
               robot_hitbox.x -= 8
            if bot_move == 'down':
               robot_hitbox.y += 8
            robot_movement.pop(0)

            surface.blit(santa_icon, (robot_hitbox.x, robot_hitbox.y))
            print("Santa move: x= %s y= %s" % (robot_hitbox.x, robot_hitbox.y))
        else:
            print("No path available")
            surface.blit(santa_icon, (robot_hitbox.x, robot_hitbox.y))

        pygame.draw.circle(surface, pygame.Color('green'), *get_circle(*start))
        pygame.draw.circle(surface, pygame.Color('magenta'), *get_circle(*path_head))

        # Gift render
        gift_obj.render(surface, scroll)

        # Score handling
        surface.blit(draw_text('Score:' + str(score_counter), 'BULKYPIX.TTF', 12, red), (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                # Moving
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_a:
                    moving_left = True

                # Jump
                if event.key == pygame.K_SPACE:
                    if air_timer < 6:
                        player_jump_sound.play()
                        player_jump = -8

                # Back to menu
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.KEYUP:

                # Moving
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_a:
                    moving_left = False

            if event.type == pygame.QUIT:
                quit()

        screen.blit(pygame.transform.scale(surface, (window_size[0], window_size[1])), (0, 0))
        pygame.display.update()
        clock.tick(60)

# Options
def options():

    while True:
        # Screen filling
        surface.fill(sky_blue)

        # Snow falling
        snow_falling(surface, surface_size, white)

        # Logo
        surface.blit(draw_text('Options', 'BULKYPIX.TTF', 25, white), (surface_size[0] / 4 + 32, surface_size[1] / 12))

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                # Back to menu
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.QUIT:
                quit()

        screen.blit(pygame.transform.scale(surface, (window_size[0], window_size[1])), (0, 0))
        pygame.display.update()
        clock.tick(60)

# Main menu call
main_menu()