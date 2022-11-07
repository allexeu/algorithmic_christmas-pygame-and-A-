def change_action(action, frame, new_action):
    if action != new_action:
        action = new_action
        frame = 0

    return new_action, frame