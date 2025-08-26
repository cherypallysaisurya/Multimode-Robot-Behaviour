import numpy as np

from go1_py.state import Robot


def distanceToWarning(distance):
    if distance > 30:
        return np.float64(0)
    elif distance < 10:
        return np.float64(1)
    else:
        return 0.2 + (0.8 * (30 - distance)) / 20


def parse(payload):
    robot = Robot()
    robot.temps = payload[8:28]
    if len(payload) > 28:
        robot.mode = payload[28]
        robot.gaitType = payload[29]
        robot.obstacles = payload[30:34]
        if robot.mode == 2:
            match robot.gaitType:
                case 1:
                    robot.state = "walk"
                case 2:
                    robot.state = "run"
                case 3:
                    robot.state = "climb"
        robot.distanceWarning.front = distanceToWarning(robot.obstacles[0])
        robot.distanceWarning.left = distanceToWarning(robot.obstacles[1])
        robot.distanceWarning.right = distanceToWarning(robot.obstacles[2])
        robot.distanceWarning.back = distanceToWarning(robot.obstacles[3])
    if len(payload) >= 44:
        match payload[0]:
            case 1:
                name = "Laikago"
            case 2:
                name = "Aliengo"
            case 3:
                name = "A1"
            case 4:
                name = "Go1"
            case 5:
                name = "B1"
        match payload[1]:
            case 1:
                model = "AIR"
            case 2:
                model = "PRO"
            case 3:
                model = "EDU"
            case 4:
                model = "PC"
            case 5:
                model = "XX"
        robot.sn.product = f"{name}_{model}"
        if payload[2] < 255:
            robot.sn.id = f"{payload[2]}-{payload[3]}-{payload[4]}[{payload[5]}]"
        if payload[36] < 255:
            robot.version.hardware = f"{payload[36]}.{payload[37]}.{payload[38]}"
        robot.version.software = f"{payload[39]}.{payload[40]}.{payload[41]}"
    return robot
