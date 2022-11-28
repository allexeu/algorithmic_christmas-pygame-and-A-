def robot_movement_path(robot_path):
    robot_movement = []
    for index, path in enumerate(robot_path[::-1]):
        if (len(robot_path) - index - 1) - 1 > -1:
            if path[0] == robot_path[(len(robot_path) - index - 1) - 1][0]:
                if path[1] < robot_path[(len(robot_path) - index - 1) - 1][1]:
                    robot_movement.append("down")
                    robot_movement.append("down")
                    robot_movement.append("down")
                    robot_movement.append("down")
                if path[1] > robot_path[(len(robot_path) - index - 1) - 1][1]:
                    robot_movement.append("top")
                    robot_movement.append("top")
                    robot_movement.append("top")
                    robot_movement.append("top")
            else:
                if path[0] < robot_path[(len(robot_path) - index - 1) - 1][0]:
                    robot_movement.append("right")
                    robot_movement.append("right")
                    robot_movement.append("right")
                    robot_movement.append("right")
                elif path[0] > robot_path[(len(robot_path) - index - 1) - 1][0]:
                    robot_movement.append("left")
                    robot_movement.append("left")
                    robot_movement.append("left")
                    robot_movement.append("left")

    return robot_movement
