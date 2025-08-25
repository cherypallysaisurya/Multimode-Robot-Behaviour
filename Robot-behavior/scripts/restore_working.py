#!/usr/bin/env python3
"""
RESTORE TO WORKING STATE - Single Command Recovery

Run this script to restore the robot behavior simulator to the working state
where robot position and trail visualization are accurate.

Usage: python restore_working.py
"""

import os
import shutil
from pathlib import Path

def restore_working_state():
    """Restore all files to the working state from August 22, 2025"""
    
    base_dir = Path(__file__).parent
    
    print("🔧 Restoring Robot Behavior Simulator to WORKING state...")
    print("=" * 60)
    
    # 1. Restore examples/minimal_api_examples.py
    example_content = '''from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def simple_example():
    """Super simple student example with real-time visualization"""
    
    # Create robot world
    program = create_robot_program(5, 5, 0, 1)
    program.add_wall(2, 0)
    program.add_wall(3, 1)
    
    # Define robot movements
    def my_moves():
        program.robot.move('right')
        program.robot.move('right') 
        program.robot.move('up')
        program.robot.move('up')
    
    # Run with automatic visualization
    run_with_visualization(program, my_moves)

if __name__ == "__main__":
    simple_example()
'''
    
    example_file = base_dir / "examples" / "minimal_api_examples.py"
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write(example_content)
    print(f"✅ Restored: {example_file}")
    
    # 2. Restore the fixed run_with_visualization function in minimal_api.py
    api_file = base_dir / "robot_behavior" / "minimal_api.py"
    
    # Read current content
    with open(api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the run_with_visualization function
    fixed_function = '''def run_with_visualization(program, moves_function):
    """
    Run student code with automatic real-time visualization.
    
    Args:
        program: Robot program created with create_robot_program()
        moves_function: Function containing robot moves
        
    Example:
        program = create_robot_program(5, 5, 0, 1)
        def my_moves():
            program.robot.move('right')
            program.robot.move('up')
        run_with_visualization(program, my_moves)
    """
    import threading
    import platform
    import time
    from robot_behavior.core.robot import Position
    
    def enhanced_moves():
        """Wrapper that adds simulator notifications to basic robot moves."""
        time.sleep(1)  # Wait for GUI to start
        
        # Monkey patch the robot's move method to notify simulator
        original_move = program.robot.move
        
        def move_with_notification(direction):
            old_pos = Position(program.robot.position.x, program.robot.position.y)
            success = original_move(direction)
            new_pos = program.robot.get_position()
            
            # Notify simulator about the move
            if hasattr(program, 'simulator') and program.simulator.running:
                program.simulator.robot_moved(old_pos, new_pos, success)
                time.sleep(0.5)  # Small delay for visualization
            
            return success
        
        program.robot.move = move_with_notification
        
        # Run the student's moves
        moves_function()
        
        # Restore original move method
        program.robot.move = original_move
    
    if platform.system() == "Darwin":  # macOS - no threading
        print("🍎 macOS detected - running moves then showing result")
        enhanced_moves()
        program.start()
    else:  # Windows/Linux - real-time with threading
        print("🖥️ Windows/Linux detected - real-time visualization")
        movement_thread = threading.Thread(target=enhanced_moves)
        movement_thread.daemon = True
        movement_thread.start()
        program.start()'''
    
    # Find and replace the function
    import re
    pattern = r'def run_with_visualization\(.*?\n(?:.*?\n)*?        program\.start\(\)'
    new_content = re.sub(pattern, fixed_function, content, flags=re.DOTALL)
    
    with open(api_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ Restored: {api_file} (fixed run_with_visualization)")
    
    print("\n🎉 WORKING STATE RESTORED!")
    print("=" * 60)
    print("✅ Robot position accuracy: FIXED")
    print("✅ Trail visualization: FIXED") 
    print("✅ Real-time sync: FIXED")
    print("\n🧪 Test with:")
    print('   cd "d:\\Robot-behavior"')
    print('   $env:PYTHONPATH="d:\\Robot-behavior"')
    print('   python examples/minimal_api_examples.py')
    print("\n📊 Expected: Robot at (2,3) with L-shaped red trail")

if __name__ == "__main__":
    restore_working_state()
