#!/usr/bin/env python3
"""
Student Template - Robot Programming Exercise

Use this template to write your own robot algorithms!
"""

from robot_behavior.minimal_api import create_robot_program
import time

def my_robot_algorithm():
    """
    Write your robot algorithm here!
    
    Available commands:
    - program.move_with_delay('up')      # Move up
    - program.move_with_delay('down')    # Move down  
    - program.move_with_delay('left')    # Move left
    - program.move_with_delay('right')   # Move right
    - program.move_with_delay('backward') # Move backward
    - program.add_wall(x, y)             # Add wall at position (x,y)
    - program.robot.get_position()       # Get current position
    """
    
    print("🤖 My Robot Algorithm")
    print("=" * 30)
    
    # Create robot world (change size and starting position as needed)
    program = create_robot_program(width=8, height=8, start_x=0, start_y=0)
    
    # Add walls to create obstacles (optional)
    # program.add_wall(3, 2)
    # program.add_wall(3, 3)
    # program.add_wall(3, 4)
    
    # Start the visual display
    import threading
    gui_thread = threading.Thread(target=program.start)
    gui_thread.daemon = True
    gui_thread.start()
    time.sleep(1)  # Wait for GUI to load
    
    # TODO: Write your movement algorithm here!
    # Example: Make the robot move in a square pattern
    
    # program.move_with_delay('right')
    # program.move_with_delay('right')
    # program.move_with_delay('up')
    # program.move_with_delay('up')
    # program.move_with_delay('left')
    # program.move_with_delay('left')
    # program.move_with_delay('down')
    # program.move_with_delay('down')
    
    print("✅ Algorithm complete!")
    
    # Keep window open for 5 seconds to see the result
    time.sleep(5)

if __name__ == "__main__":
    my_robot_algorithm()
