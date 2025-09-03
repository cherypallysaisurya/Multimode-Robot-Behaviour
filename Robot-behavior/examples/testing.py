

from robot_behavior.minimal_api import create_robot_program, run_with_visualization


def main():
    program = create_robot_program(5, 5, 0, 0, mode="simulator")
    program.add_wall(3, 0)
    program.add_wall(4, 1)

    def moves():
        program.robot.move('right')
        program.robot.move('right')
        program.robot.move('up')
        program.robot.move('right')
        program.robot.move('up')

    run_with_visualization(program, moves, move_delay=0.5)


if __name__ == "__main__":
    main()
