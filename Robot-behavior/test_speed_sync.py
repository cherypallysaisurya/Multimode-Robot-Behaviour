from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def test_fast_speed():
    print("🏃 Testing FAST speed (0.2s delay)")
    program = create_robot_program(5, 5, 0, 1)
    program.add_wall(2, 0)
    
    def fast_moves():
        program.robot.move('right')
        program.robot.move('right') 
        program.robot.move('up')
    
    run_with_visualization(program, fast_moves, move_delay=0.2)

def test_slow_speed():
    print("🐌 Testing SLOW speed (2.0s delay)")
    program = create_robot_program(5, 5, 0, 1)
    program.add_wall(2, 0)
    
    def slow_moves():
        program.robot.move('right')
        program.robot.move('right') 
        program.robot.move('up')
    
    run_with_visualization(program, slow_moves, move_delay=2.0)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "slow":
        test_slow_speed()
    else:
        test_fast_speed()
