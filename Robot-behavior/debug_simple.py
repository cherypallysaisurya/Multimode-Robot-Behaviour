from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def debug_example():
    """Simple debug example with just 2 moves"""
    
    # Create robot world
    program = create_robot_program(4, 4, 0, 0)
    
    # Define robot movements
    def my_moves():
        program.robot.move('right')
        program.robot.move('up')
    
    run_with_visualization(program, my_moves, move_delay=1.0)

if __name__ == "__main__":
    debug_example()
