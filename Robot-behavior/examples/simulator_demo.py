from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def main():
    program = create_robot_program(8, 6, 0, 0, mode="simulator")
    # Add a few sample walls
    for x, y in [(3,0),(3,1),(4,2),(6,4)]:
        program.add_wall(x, y)

    def moves():
        for d in ['right','right','up','up','right','up','right','right','down']:
            program.robot.move(d)

    run_with_visualization(program, moves, move_delay=0.8)

if __name__ == '__main__':
    main()
