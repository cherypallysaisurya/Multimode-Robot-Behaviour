from myrobot import create_robot_program

def test_sim_move():
    program = create_robot_program(mode='simulator', width=5, height=5)
    assert program.robot.get_position().x == 0
    program.robot.move('up')
    assert program.robot.get_position().y == 1

def test_invalid_direction_stops():
    program = create_robot_program(mode='simulator')
    ok = program.robot.move('diagonal')
    assert not ok
