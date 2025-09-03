# 🎓 Quick Start Template for Students

from unified_robot import create_robot_program, run_with_visualization

def my_robot_program():
    """
    Copy this template and add your own robot movements!
    
    Instructions:
    1. Copy this file: student_template.py -> my_program.py
    2. Edit the moves() function below
    3. Run: python my_program.py
    """
    
    # Create your robot program
    # Uncomment one of these options:
    
    # Option 1: Default settings (8x8 grid, start at 0,0)
    program = create_robot_program()
    
    # Option 2: Custom grid size
    # program = create_robot_program(grid_width=10, grid_height=6)
    
    # Option 3: Custom starting position
    # program = create_robot_program(start_x=3, start_y=2)
    
    # Option 4: Everything custom
    # program = create_robot_program(grid_width=12, grid_height=8, start_x=4, start_y=3)
    
    # Add walls (only works in simulator mode)
    program.add_wall(2, 2)
    program.add_wall(3, 3)
    
    # Define your robot movements here!
    def moves():
        """
        Add your robot.move() commands here.
        Available directions: "up", "down", "left", "right"
        """
        program.robot.move("right")
        program.robot.move("up")
        program.robot.move("left")
        program.robot.move("down")
        
        # Add more movements here:
        # program.robot.move("right")
        # program.robot.move("right")
        # program.robot.move("up")
    
    # Run your program
    run_with_visualization(program, moves)

if __name__ == "__main__":
    print("🤖 My Robot Program")
    print("=" * 20)
    print("Starting robot...")
    my_robot_program()
    print("✅ Program complete!")
