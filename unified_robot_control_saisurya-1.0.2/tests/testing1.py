from myrobot import create_robot_program, run_with_visualization


def test_simulator():
    """Test simulator mode"""
    program = create_robot_program(5, 5, 0, 0, mode="simulator")
    program.add_wall(3, 0)
    program.add_wall(4, 1)

    def moves():
        for direction in ("right", "right", "up", "right", "up"):
            program.robot.move(direction)

    run_with_visualization(program, moves, move_delay=0.5)


def test_real_robot():
    """Test real robot mode (with mock fallback)"""
    program = create_robot_program(5, 5, 0, 0, mode="real")
    # walls ignored in real mode
    program.add_wall(3, 0)  
    program.add_wall(4, 1)

    def moves():
        for direction in ("right", "right", "up", "right", "up"):
            program.robot.move(direction)

    run_with_visualization(program, moves, move_delay=0.5)


def main() -> None:
    # Students can easily switch by commenting/uncommenting:
    
    # Simulator mode (visual GUI):
    test_simulator()
    
    # Real robot mode (or mock if no hardware):
    # test_real_robot()


if __name__ == "__main__":  
    main()
