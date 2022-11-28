# General imports
import random

# Pygmae import
import pygame
pygame.init()

# Clock init
clock = pygame.time.Clock()

# Astar import
from A_star import A_Star

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
from path_builder import path_builder
from robot_movement_path import robot_movement_path
from path_map_render import path_map_render
from adjacency_dictionary_builder import adj_dict_builder

# Main colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
sky_blue = (146, 244, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255,165,0)
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

# Edu level variable for changing levels
is_edu = False

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
                if is_edu:
                    edu_level()
                else:
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

    # Player hitbox
    santa_hitbox = pygame.Rect(0, 14 * 16, tile_size, tile_size)

    # Robot hitbox
    robot_x = 15
    robot_y = 4
    robot_hitbox = pygame.Rect(23 * 16, 13 * 16, tile_size, tile_size)

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
    robot_flip = False

    # Animation database
    # for loading animations of the whole level
    anim_names_database = {}
    anim_sprites_database = {}

    # Robot database
    robot_names_database = {}
    robot_sprites_database = {}

    # Player idle animation
    anim_names_database['idle'] = anim_load(anim_sprites_database, 'santa', 'idle', [45, 45])
    # Player run animation
    anim_names_database['run'] = anim_load(anim_sprites_database, 'santa', 'run', [15, 15])
    # Player jump animation
    anim_names_database['jump'] = anim_load(anim_sprites_database, 'santa', 'jump', [15])

    # Player idle animation
    robot_names_database['idle'] = anim_load(robot_sprites_database, 'robot', 'idle', [45, 45])
    # Player run animation
    robot_names_database['run'] = anim_load(robot_sprites_database, 'robot', 'run', [15, 15])
    # Player jump animation
    robot_names_database['jump'] = anim_load(robot_sprites_database, 'robot', 'jump', [15])

    # For animations work
    player_frame = 0
    robot_frame = 0
    player_action = 'idle'
    robot_action = 'idle'

    # Santa
    santa_tile = pygame.image.load("game_core/sprites/robot/robot.png")
    # Robot
    robot_tile = pygame.image.load("game_core/sprites/robot/robot.png")

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

    # Path map
    path_map = path_map_load('level3_path_map.txt')

    # Adjacency dictionary
    adj_dict = adj_dict_builder(path_map)

    # Start point
    start = (23, 13)

    # Goal
    goal = (gift_pos[0] / 16, gift_pos[1] / 16)

    # Visited points
    visited = A_Star(start, goal, adj_dict)

    # Robot path
    robot_path = path_builder(goal, visited)

    # Robot movement path
    robot_movement = robot_movement_path(robot_path)

    # Robot tick
    robot_tick = 0

    while True:
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
            player_position[0] += 2
        if moving_left:
            player_position[0] -= 2

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

        # Player collision with gift handling
        # Delay before showing score menu
        if gift_obj.hitbox_collision(santa_hitbox, scroll):
            coin_sound.play()
            score(True, False)

        # Robot collision with gift
        if robot_hitbox.colliderect(gift_obj.get_hitbox(scroll)):
            coin_sound.play()
            score(False, True)

        # Robot movement handling
        # Robot_delay
        robot_tick += 1
        if (len(robot_movement) > 0 and robot_tick % 2 == 0):
            bot_move = robot_movement[0]
            if bot_move == 'top':
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'jump')
                robot_hitbox.y -= 4
            if bot_move == 'right':
                robot_flip = False
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'run')
                robot_hitbox.x += 4
            if bot_move == 'left':
                robot_flip = True
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'run')
                robot_hitbox.x -= 4
            if bot_move == 'down':
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'jump')
                robot_hitbox.y += 4
            robot_movement.pop(0)

        # Robot frames animation incrementing
        robot_frame += 1
        if robot_frame >= len(robot_names_database[robot_action]):
            robot_frame = 0

        # Current player sprite
        robot = robot_sprites_database[robot_names_database[robot_action][robot_frame]]

        # Robot render
        surface.blit(pygame.transform.flip(robot, robot_flip, False), (robot_hitbox.x, robot_hitbox.y))

        # Gift render
        gift_obj.render(surface, scroll)

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

# Score menu variables
round_num = 0
santa_score = 0
robot_score = 0
def score(player_score, bot_score):
    global round_num
    global santa_score
    global robot_score

    round_num += 1

    if player_score:
        santa_score += 1

    if bot_score:
        robot_score += 1

    delay_counter = 0
    while True:
        # Screen filling
        surface.fill(sky_blue)

        # Snow falling
        snow_falling(surface, surface_size, white)

        # Round logo
        surface.blit(draw_text('Round:' + str(round_num), 'BULKYPIX.TTF', 25, white),
                     (surface_size[0] / 4 + 32, surface_size[1] / 12))

        # Santa counter
        surface.blit(draw_text('Santa:' + str(santa_score), 'BULKYPIX.TTF', 25, red),
                     (surface_size[0] / 8, surface_size[1] / 4))
        # Enemy counter
        surface.blit(draw_text('Robot:' + str(robot_score), 'BULKYPIX.TTF', 25, blue),
                     (surface_size[0] / 2 + 32, surface_size[1] / 4))

        # Level turning on delay
        delay_counter += 1
        if delay_counter == 120:
            level_1()

        screen.blit(pygame.transform.scale(surface, (window_size[0], window_size[1])), (0, 0))
        pygame.display.update()
        clock.tick(60)

# Edu level:
def edu_level():
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

    # Player hitbox
    santa_hitbox = pygame.Rect(0, 14 * 16, tile_size, tile_size)

    # Robot hitbox
    robot_x = 15
    robot_y = 4
    robot_hitbox = pygame.Rect(23 * 16, 13 * 16, tile_size, tile_size)

    # Player movement
    moving_right = False
    moving_left = False
    player_jump = 0
    air_timer = 0

    # Scroll
    true_scroll = [0, 0]

    # Background objects
    background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                          [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

    # Flip
    player_flip = False
    robot_flip = False

    # Animation database
    # for loading animations of the whole level
    anim_names_database = {}
    anim_sprites_database = {}

    # Robot database
    robot_names_database = {}
    robot_sprites_database = {}

    # Player idle animation
    anim_names_database['idle'] = anim_load(anim_sprites_database, 'santa', 'idle', [45, 45])
    # Player run animation
    anim_names_database['run'] = anim_load(anim_sprites_database, 'santa', 'run', [15, 15])
    # Player jump animation
    anim_names_database['jump'] = anim_load(anim_sprites_database, 'santa', 'jump', [15])

    # Player idle animation
    robot_names_database['idle'] = anim_load(robot_sprites_database, 'robot', 'idle', [45, 45])
    # Player run animation
    robot_names_database['run'] = anim_load(robot_sprites_database, 'robot', 'run', [15, 15])
    # Player jump animation
    robot_names_database['jump'] = anim_load(robot_sprites_database, 'robot', 'jump', [15])

    # For animations work
    player_frame = 0
    robot_frame = 0
    player_action = 'idle'
    robot_action = 'idle'

    # Santa
    santa_tile = pygame.image.load("game_core/sprites/robot/robot.png")
    # Robot
    robot_tile = pygame.image.load("game_core/sprites/robot/robot.png")

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

    # Path map
    path_map = path_map_load('level3_path_map.txt')

    # Adjacency dictionary
    graph = adj_dict_builder(path_map)
    print(path_map)
    # Start point
    start = (23, 13)

    # Goal
    goal = (gift_pos[0] / 16, gift_pos[1] / 16)

    # Visited points
    visited = A_Star(start, goal, graph)

    # Robot path
    robot_path = path_builder(goal, visited)

    # Robot movement path
    robot_movement = robot_movement_path(robot_path)

    # Robot tick
    robot_tick = 0

    def get_circle(x, y):
        return (x * 16 + 16 // 2, y * 16 + 16 // 2), 16 // 4

    while True:
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

        # Player collision with gift handling
        # Delay before showing score menu
        if gift_obj.hitbox_collision(santa_hitbox, scroll):
            coin_sound.play()
            edu_level()

        # Robot collision with gift
        if robot_hitbox.colliderect(gift_obj.get_hitbox(scroll)):
            coin_sound.play()
            edu_level()

        # Robot movement handling
        # Robot_delay
        robot_tick += 1
        if (len(robot_movement) > 0 and robot_tick % 2 == 0):
            bot_move = robot_movement[0]
            if bot_move == 'top':
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'jump')
                robot_hitbox.y -= 4
            if bot_move == 'right':
                robot_flip = False
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'run')
                robot_hitbox.x += 4
            if bot_move == 'left':
                robot_flip = True
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'run')
                robot_hitbox.x -= 4
            if bot_move == 'down':
                robot_action, robot_frame = change_action(robot_action, robot_frame, 'jump')
                robot_hitbox.y += 4
            robot_movement.pop(0)

        # Robot frames animation incrementing
        robot_frame += 1
        if robot_frame >= len(robot_names_database[robot_action]):
            robot_frame = 0

        # Edu visualization
        # print(visited)
        for algo_path in visited:
            pygame.draw.circle(surface, red, *get_circle(*algo_path))

        for path in robot_path:
            pygame.draw.circle(surface, blue, *get_circle(*path))

        pygame.draw.circle(surface, white, *get_circle(*start))

        # Current robot sprite
        robot = robot_sprites_database[robot_names_database[robot_action][robot_frame]]

        # Robot render
        surface.blit(pygame.transform.flip(robot, robot_flip, False), (robot_hitbox.x, robot_hitbox.y))

        # Gift render
        gift_obj.render(surface, scroll)

        # Path map render
        path_map_render(surface, path_map, orange, yellow)

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
        clock.tick(10)

# Options
def options():
    # Edu level variable
    global is_edu

    # Buttons list
    buttons = [pygame.Rect(surface_size[0] / 4 + 24, surface_size[1] / 4 + 24, 150, 30),
               pygame.Rect(surface_size[0] / 4 + 24, surface_size[1] / 4 + 24 * 3, 150, 30),
               pygame.Rect(surface_size[0] / 4 + 24, surface_size[1] / 4 + 24 * 5, 150, 30)]

    # Variables for choosing options and menu
    choose_state = 2
    choose_option = {2: 'Arcade', 1: 'Edu'}
    is_chose = False
    choose_mark_pos = [surface_size[0] / 4, surface_size[1] / 4 + 28]

    while True:
        # Screen filling
        surface.fill(sky_blue)

        # Snow falling
        snow_falling(surface, surface_size, white)

        # Logo
        surface.blit(draw_text('Options', 'BULKYPIX.TTF', 25, white), (surface_size[0] / 4 + 32, surface_size[1] / 12))

        # Buttons
        pygame.draw.rect(surface, white, buttons[0])
        surface.blit(draw_text('Arcade', 'BULKYPIX.TTF', 25, black), (surface_size[0] / 3 + 10, surface_size[1] / 4 + 28))
        pygame.draw.rect(surface, white, buttons[1])
        surface.blit(draw_text('Edu', 'BULKYPIX.TTF', 25, black), (surface_size[0] / 2 - 24, surface_size[1] / 4 + 25 * 3))

        # Choosing option navigation
        if choose_state > 2:
            choose_state = 1
        if choose_state == 2:
            surface.blit(draw_text('>', 'BULKYPIX.TTF', 25, white), (choose_mark_pos[0], choose_mark_pos[1]))
        if choose_state == 1:
            surface.blit(draw_text('>', 'BULKYPIX.TTF', 25, white), (choose_mark_pos[0], choose_mark_pos[1] + 48))
        if choose_state < 1:
            choose_state = 2

        # Chose option check
        if is_chose == True:
            if choose_option[choose_state] == 'Arcade':
                is_edu = False
            if choose_option[choose_state] == 'Edu':
                is_edu = True

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    choose_state += 1
                if event.key == pygame.K_DOWN:
                    choose_state -= 1

                if event.key == pygame.K_SPACE:
                    is_chose = True

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