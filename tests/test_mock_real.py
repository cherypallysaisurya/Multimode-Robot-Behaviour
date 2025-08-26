import os
from myrobot import create_robot_program

def test_mock_real_moves():
    os.environ['ROBOT_BEHAVIOR_HARDWARE_MOCK'] = '1'
    program = create_robot_program(mode='real')
    program.robot.move('up')
    program.robot.move('left')
    # just ensure no exception and mode recorded if controller exposes log
    assert program.mode == 'real'
