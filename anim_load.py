import pygame

def anim_load(loaded_animations, name, anim_type, frames_duration):
    frames_names = []
    n = 0
    for frame in frames_duration:
        frame_name = anim_type + '_' + str(n)
        frame_path = 'game_core/sprites/' + name + '/' + anim_type + '/' + frame_name + '.png'
        frame_sprite = pygame.image.load(frame_path)
        loaded_animations[frame_name] = frame_sprite.copy()
        for _ in range(frame):
            frames_names.append(frame_name)

        n += 1

    return frames_names