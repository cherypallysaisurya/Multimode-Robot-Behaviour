
# Ensure local robot_behavior is used
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def simple_example():
    
    
    # Create robot world
    program = create_robot_program(5, 5, 0, 1)
    program.add_wall(2, 0)
    program.add_wall(4, 1)
    
    # Define robot movements
    def my_moves():
        program.robot.move('right')
        program.robot.move('right') 
        program.robot.move('up')
        program.robot.move('right') 
        program.robot.move('up')
    

    run_with_visualization(program, my_moves, move_delay=0.5)

if __name__ == "__main__":
    simple_example()