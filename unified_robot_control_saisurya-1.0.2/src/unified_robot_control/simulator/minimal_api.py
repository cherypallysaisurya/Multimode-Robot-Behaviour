"""
Minimal Robot API for Educational Programming

This module provides the core robot movement API with strict obstacle
detection and immediate simulation stopping on illegal moves.

Students must implement all complex behaviors using only these basic commands:

- robot.move(direction) - Move one cell in specified direction  
- robot.get_position() - Get current position
- robot.load_maze(layout) - Load instructor-defined maze
- robot.reset_simulation() - Reset after hitting obstacle

The simulation stops immediately on illegal moves, requiring students
to handle error cases and implement proper movement logic.
"""

from .core.robot import Robot, Position
import threading
import time as time_module
import tkinter as tk
from tkinter import messagebox
import os

def create_robot_program(width=10, height=10, start_x=0, start_y=0, mode: str = 'simulator', host: str | None = None, initial_mode: str | None = "Walk"):
    """
    Create a robot program with the specified parameters.
    
    Args:
        width: Grid width (3-20)
        height: Grid height (3-20) 
        start_x: Starting X position
        start_y: Starting Y position
        mode: 'simulator' or 'real' (can be overridden by ROBOT_MODE environment variable)
        host: Host for real robot connection
        initial_mode: Initial robot mode for real hardware
        
    Returns:
        RobotProgram: Configured robot program instance
    """
    # Check environment variable override first (priority: env var > parameter > default)
    env_mode = os.environ.get('ROBOT_MODE')
    if env_mode:
        mode = env_mode
        print(f"🌍 Using ROBOT_MODE environment variable: {mode}")
    
    # Validate grid size
    if not (3 <= width <= 20) or not (3 <= height <= 20):
        # Create a temporary root window for the error dialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        messagebox.showerror(
            "Invalid Grid Size", 
            f"Grid size must be between 3x3 and 20x20.\nRequested: {width}x{height}\nPlease use a size between 3 and 20 for both width and height."
        )
        root.destroy()
        raise ValueError(f"Grid size must be between 3x3 and 20x20. Got {width}x{height}")
    
    if mode == 'real':
        # Import and use real robot hardware
        from ..robot_hardware.go1_interface import Go1Interface
        
        print("Initializing real robot hardware...")
        robot_interface = Go1Interface(host=host, initial_mode=initial_mode)
        robot = Robot(robot_interface)
        
        return RobotProgram(robot, None, mode='real')
    else:
        # Use simulator
        from .simulator.enhanced_simulator import EnhancedSimulator
        
        robot = Robot()
        # Set robot position
        robot.position = Position(start_x, start_y)
        
        # Create simulator with robot and grid dimensions
        simulator = EnhancedSimulator(robot, cell_size=60)
        simulator.grid_width = width
        simulator.grid_height = height
        
        # Link robot and simulator
        robot.set_simulator(simulator)
        
        return RobotProgram(robot, simulator, mode='simulator')


def run_with_visualization(robot_program, student_function, move_delay: float = 0.5):
    """
    Run student code with real-time visualization.
    
    Args:
        robot_program: Robot program instance
        student_function: Function containing student's robot control code
        move_delay: Delay between moves for animation (seconds)
    """
    if robot_program.mode == 'real':
        # Real robot - just run the student function
        try:
            student_function(robot_program.robot)
        except Exception as e:
            print(f"Error in student code: {e}")
        finally:
            robot_program.robot.disconnect()
        return
    
    # Simulator mode - set up visualization
    program = robot_program
    
    def enhance_robot_moves(original_move):
        """Enhance robot moves with visualization updates and collision detection."""
        def move_with_notification(direction):
            old_pos = program.robot.get_position()
            success = original_move(direction)
            new_pos = program.robot.get_position()
            
            # Check if simulation stopped due to wall collision
            if hasattr(program.robot, 'is_simulation_stopped') and program.robot.is_simulation_stopped():
                # Stop execution immediately with clear error message
                raise RuntimeError("Simulation stopped due to wall collision")
            
            # Notify simulator about the move - with better checking and move_delay
            if hasattr(program, 'simulator') and program.simulator.running and hasattr(program.simulator, 'canvas') and program.simulator.canvas:
                program.simulator.robot_moved(old_pos, new_pos, success, move_delay)
                time_module.sleep(move_delay)  # Customizable delay
            
            return success
        return move_with_notification
    
    # Enhance the robot's move method
    program.robot.move = enhance_robot_moves(program.robot.move)
    
    def run_student_code():
        """Run student code in separate thread with exception handling."""
        try:
            student_function(program.robot)
        except RuntimeError as e:
            if "wall collision" in str(e):
                print(f"Program stopped: {e}")
                # Don't continue execution after wall collision
                return
            else:
                raise
        except Exception as e:
            print(f"Error in student code: {e}")
            import traceback
            traceback.print_exc()
    
    # Start student code in background thread
    code_thread = threading.Thread(target=run_student_code, daemon=True)
    code_thread.start()
    
    # Run the simulator GUI (this blocks until window closes)
    program.simulator.run()


class RobotProgram:
    """
    Container for robot and simulator instances.
    """
    def __init__(self, robot, simulator=None, mode='simulator'):
        self.robot = robot
        self.simulator = simulator 
        self.mode = mode
        
    def get_robot(self):
        """Get the robot instance."""
        return self.robot
        
    def get_simulator(self):
        """Get the simulator instance (None for real robot)."""
        return self.simulator


# Keep backward compatibility
def create_enhanced_robot_program(*args, **kwargs):
    """Backward compatibility wrapper."""
    return create_robot_program(*args, **kwargs)


def run_enhanced_simulation(*args, **kwargs):
    """Backward compatibility wrapper."""
    return run_with_visualization(*args, **kwargs)


# Simple maze layouts for educational use
SIMPLE_MAZE = [
    ['.', '.', '.', '#', '.', '.', '.'],
    ['.', '#', '.', '#', '.', '#', '.'], 
    ['.', '#', '.', '.', '.', '#', '.'],
    ['.', '#', '#', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.', '.', '.']
]

STUDENT_MAZE = [
    ['S', '.', '.', '#', '.', '.', '.', '.'],
    ['.', '#', '.', '#', '.', '#', '.', '.'],
    ['.', '#', '.', '.', '.', '#', '.', '.'], 
    ['.', '.', '.', '#', '#', '#', '.', '.'],
    ['#', '#', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '#', '.', '#', '#', '.'],
    ['.', '#', '.', '#', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
]


def run_fast(program, moves_function):
    """Run with fast animation (0.2s delay)."""
    return run_with_visualization(program, moves_function, move_delay=0.2)


def run_slow(program, moves_function):
    """Run with slow animation (1.0s delay)."""
    return run_with_visualization(program, moves_function, move_delay=1.0)


def run_normal(program, moves_function):
    """Run with normal animation (0.5s delay)."""
    return run_with_visualization(program, moves_function, move_delay=0.5)


def load_maze_from_file(filename):
    """Load maze layout from file."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        maze = []
        for line in lines:
            row = list(line.strip())
            if row:  # Skip empty lines
                maze.append(row)
        return maze
    except FileNotFoundError:
        print(f"❌ Maze file '{filename}' not found")
        return None
    except Exception as e:
        print(f"❌ Error loading maze: {e}")
        return None


def run_demo_example():
    """Run a basic demo of the robot simulator."""
    print("🎮 Starting Robot Demo...")
    
    def demo_moves(robot):
        """Demo movement sequence."""
        robot.move("right")
        robot.move("right") 
        robot.move("up")
        robot.move("left")
        robot.move("up")
        robot.move("right")
    
    # Create demo program
    program = create_robot_program(width=8, height=6, start_x=1, start_y=1)
    program.robot.add_wall(3, 2)
    program.robot.add_wall(4, 3)
    
    print("🎯 Demo: Watch the robot navigate!")
    run_with_visualization(program, demo_moves)
