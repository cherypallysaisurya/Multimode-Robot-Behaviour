# 🎓 Student Example - Basic Robot Control

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from unified_robot_control.simulator.minimal_api import create_robot_program, run_with_visualization

def basic_movement_example():
    """
    Basic robot movement example - works with both simulator and real robot!
    """
    # Create a robot program (uses default 10x10 grid)
    program = create_robot_program()
    
    # Add some walls for the simulator (ignored in real robot mode)
    program.robot.add_wall(2, 1)
    program.robot.add_wall(3, 2)
    program.robot.add_wall(1, 3)
    
    # Define your robot movements
    def moves(robot):
        """Your robot movement sequence"""
        robot.move("right")  # Move right
        robot.move("right")  # Move right again
        robot.move("up")     # Move up
        robot.move("left")   # Move left
        robot.move("up")     # Move up
        robot.move("right")  # Move right
    
    # Run the program with visualization
    run_with_visualization(program, moves)

def custom_grid_example():
    """
    Example with custom grid size and starting position
    """
    # Create a larger grid starting from position (2, 1)
    program = create_robot_program(
        width=10, 
        height=6, 
        start_x=2, 
        start_y=1
    )
    
    def moves(robot):
        """Movements for larger grid"""
        for i in range(3):
            robot.move("right")
        for i in range(2):
            robot.move("up")
        for i in range(2):
            robot.move("left")
    
    run_with_visualization(program, moves)

def maze_navigation_example():
    """
    Example with obstacle navigation
    """
    # Small grid with obstacles
    program = create_robot_program(grid_width=6, grid_height=6)
    
    # Create a simple maze
    program.add_wall(1, 1)
    program.add_wall(2, 1)
    program.add_wall(3, 1)
    program.add_wall(1, 2)
    program.add_wall(3, 2)
    program.add_wall(3, 3)
    
    def moves():
        """Navigate around obstacles"""
        program.robot.move("up")     # Try to go up
        program.robot.move("up")     # Go up again
        program.robot.move("right")  # Go right
        program.robot.move("right")  # Go right again
        program.robot.move("up")     # Go up
        program.robot.move("right")  # Go right
    
    run_with_visualization(program, moves)

if __name__ == "__main__":
    print("🤖 Student Robot Examples")
    print("=" * 30)
    print("Choose an example:")
    print("1. Basic Movement")
    print("2. Custom Grid")
    print("3. Maze Navigation")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print("Running Basic Movement Example...")
        basic_movement_example()
    elif choice == "2":
        print("Running Custom Grid Example...")
        custom_grid_example()
    elif choice == "3":
        print("Running Maze Navigation Example...")
        maze_navigation_example()
    else:
        print("Invalid choice. Running Basic Movement Example...")
        basic_movement_example()
