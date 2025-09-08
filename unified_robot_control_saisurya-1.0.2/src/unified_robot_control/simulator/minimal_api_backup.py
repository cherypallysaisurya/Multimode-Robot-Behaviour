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
import os
import tkinter as tk
from tkinter import messagebox
from .simulator.enhanced_simulator import RobotProgram
from .controllers import build_program, Program  # unified abstraction (simulator | real)

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
    # Check environment variable override
    env_mode = os.environ.get('ROBOT_MODE')
    if env_mode:
        mode = env_mode
        print(f"Using ROBOT_MODE environment variable: {mode}")
    
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
    """Create a new program with validation.

    Backwards compatible: existing code (without *mode*) still gets the original
    simulator behavior. When *mode='real'* a unified `Program` wrapping a Go1
    controller is returned. In simulator mode a `Program` wrapping the original
    RobotProgram is returned (legacy attributes still accessible).

    Args:
        width, height: Grid size (simulator mode only; ignored for real mode)
        start_x, start_y: Start coordinates (simulator mode only)
        mode: 'simulator' (default) or 'real'
        host: Optional hostname / IP for the real robot (real mode)

    Returns:
        Program | RobotProgram (legacy) – but consistently exposes `.robot.move()`.
    """
    # Validate grid dimensions for simulator mode
    if mode == 'simulator':
        MIN_SIZE, MAX_SIZE = 3, 20
        
        if not (MIN_SIZE <= width <= MAX_SIZE):
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror(
                "Invalid Grid Size", 
                f"❌ Grid width must be between {MIN_SIZE} and {MAX_SIZE}.\n\nYou entered: {width}\n\nPlease use a value between {MIN_SIZE}-{MAX_SIZE}."
            )
            root.destroy()
            raise ValueError(f"Grid width {width} is out of range. Must be between {MIN_SIZE} and {MAX_SIZE}.")
        
        if not (MIN_SIZE <= height <= MAX_SIZE):
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror(
                "Invalid Grid Size", 
                f"❌ Grid height must be between {MIN_SIZE} and {MAX_SIZE}.\n\nYou entered: {height}\n\nPlease use a value between {MIN_SIZE}-{MAX_SIZE}."
            )
            root.destroy()
            raise ValueError(f"Grid height {height} is out of range. Must be between {MIN_SIZE} and {MAX_SIZE}.")
        
        # Validate starting position
        if not (0 <= start_x < width):
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Invalid Starting Position", 
                f"❌ Start X position must be between 0 and {width-1}.\n\nYou entered: {start_x}"
            )
            root.destroy()
            raise ValueError(f"Start X position {start_x} is out of range. Must be between 0 and {width-1}.")
        
        if not (0 <= start_y < height):
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Invalid Starting Position", 
                f"❌ Start Y position must be between 0 and {height-1}.\n\nYou entered: {start_y}"
            )
            root.destroy()
            raise ValueError(f"Start Y position {start_y} is out of range. Must be between 0 and {height-1}.")
    
    # Check environment variable for mode override (both ways work)
    import os
    env_mode = os.getenv("ROBOT_MODE")
    if env_mode:
        mode = env_mode.lower()
        print(f"🌍 Environment override: Using mode '{mode}' (from ROBOT_MODE environment variable)")
    
    # Default to simulator if no mode specified
    if mode is None:
        mode = 'simulator'
    
    # For compatibility with tests expecting a RobotProgram object *type*, we only
    # wrap with Program. Tests rely on program.robot.* so facade preserves access.
    return build_program(width, height, start_x, start_y, mode=mode, host=host, initial_mode=initial_mode)

def run_with_visualization(program, moves_function, move_delay=1.5):
    """Run student code with visualization *or* timed playback.

        Works for both supported modes:

        - Simulator mode: launches GUI and animates moves with delay.
        - Real mode: executes moves sequentially with ``time.sleep(move_delay)``
            between moves (no GUI). Use your own speed/time kwargs in
            ``program.robot.move`` if you need custom timing – the wrapper only
            spaces the calls similarly to animation pacing.
    
    Args:
        program: Program (simulator or real)
        moves_function: Function containing robot moves
        move_delay: Delay in seconds between moves (default: 1.5)
    """
    import threading
    import time as time_module
    from .core.robot import Position

    # --- Real mode shortcut (no GUI/animation) ---
    if getattr(program, 'mode', 'simulator') == 'real':
        print("🛠️ Real mode: running moves sequentially (no GUI) ...")
        # Wrap robot.move to inject delay *after* each successful/attempted move
        original_move = program.robot.move

        def move_with_delay(direction, speed=0.5, time=1.0):
            result = original_move(direction, speed, time)
            time_module.sleep(move_delay)
            return result

        program.robot.move = move_with_delay  # type: ignore
        try:
            moves_function()
        finally:
            program.robot.move = original_move  # restore
        print("✅ Real mode sequence complete.")
        return
    
    def enhanced_moves():
        """Wrapper that adds simulator notifications to basic robot moves."""
        # Wait longer for GUI to fully initialize
        time_module.sleep(4.0)  # Increased wait time for GUI initialization
        
        # Wait until GUI is actually ready with better checking
        max_wait = 15  # Maximum 15 seconds
        wait_count = 0
        while (not hasattr(program, 'simulator') or 
               not program.simulator.running or 
               not hasattr(program.simulator, 'canvas') or 
               program.simulator.canvas is None) and wait_count < max_wait:
            time_module.sleep(0.5)
            wait_count += 0.5
            print(f"🔄 Waiting for GUI initialization... ({wait_count}s)")
        
        if wait_count >= max_wait:
            print("⚠️ GUI initialization timeout - proceeding anyway")
        else:
            print("✅ GUI is ready - starting movements")
        
        # Monkey patch the robot's move method to notify simulator
        original_move = program.robot.move
        
        def move_with_notification(direction):
            old_pos = Position(program.robot.position.x, program.robot.position.y)
            success = original_move(direction)
            new_pos = program.robot.get_position()
            
            # Notify simulator about the move - with better checking and move_delay
            if hasattr(program, 'simulator') and program.simulator.running and hasattr(program.simulator, 'canvas') and program.simulator.canvas:
                program.simulator.robot_moved(old_pos, new_pos, success, move_delay)
                time_module.sleep(move_delay)  # Customizable delay
            
            return success
        
        program.robot.move = move_with_notification
        
        # Run the student's moves with exception handling
        try:
            moves_function()
        except RuntimeError as e:
            if "Simulation stopped" in str(e):
                print("🛑 Simulation stopped due to error. Please fix your code and run again.")
                # Don't continue with remaining moves
                return
            else:
                raise  # Re-raise if it's a different error
        
        # Restore original move method
        program.robot.move = original_move
    
    # Use real-time visualization for all platforms (Windows, macOS, Linux)
    print("🖥️ Cross-platform real-time visualization")
    movement_thread = threading.Thread(target=enhanced_moves)
    movement_thread.daemon = True
    movement_thread.start()
    program.start()

def run_fast(program, moves_function):
    """Run robot with fast movement (0.5s delay)"""
    run_with_visualization(program, moves_function, move_delay=0.5)

def run_slow(program, moves_function):
    """Run robot with slow movement (2.5s delay)"""
    run_with_visualization(program, moves_function, move_delay=2.5)

def run_normal(program, moves_function):
    """Run robot with normal movement (1.0s delay)"""
    run_with_visualization(program, moves_function, move_delay=1.0)

def load_maze_from_file(filename):
    """
    Load a maze layout from a text file.
    
    File format:
    - '.' for empty space
    - '#' for wall
    - 'S' for start position
    
    Args:
        filename: Path to maze file
        
    Returns:
        List[List[str]]: 2D maze layout
    """
    try:
        with open(filename, 'r') as f:
            return [list(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        print(f"❌ Maze file not found: {filename}")
        return None
    except Exception as e:
        print(f"❌ Error loading maze: {e}")
        return None

# Export main classes and functions
__all__ = [
    'Robot',
    'Position', 
    'RobotProgram',  # legacy export
    'Program',       # new abstraction
    'create_robot_program',
    'run_with_visualization',
    'run_fast',
    'run_slow', 
    'run_normal',
    'load_maze_from_file',
    'run_demo_example',
    'SIMPLE_MAZE',
    'STUDENT_MAZE'
]

def run_demo_example():
    """
    Demo function that runs when users type 'robot-demo' command.
    Shows off the robot simulator capabilities.
    """
    import time
    
    print("🤖 Robot Behavior Simulator Demo")
    print("=" * 40)
    print("Welcome to the Robot Behavior Simulator!")
    print("Watch the robot move around and leave a red trail...")
    print()
    
    # Create demo program
    program = create_robot_program(8, 8, 0, 0)
    
    # Add some walls for interesting navigation
    walls = [(3, 1), (3, 2), (3, 3), (5, 4), (5, 5), (2, 6)]
    for x, y in walls:
        program.add_wall(x, y)
    
    # Start the visual display
    import threading
    gui_thread = threading.Thread(target=program.start)
    gui_thread.daemon = True
    gui_thread.start()
    time.sleep(1)
    
    # Demo movement sequence
    movements = [
        'right', 'right', 'up', 'up', 'up', 'right', 
        'right', 'up', 'up', 'left', 'left', 'down'
    ]
    
    print("🚀 Starting demo movement sequence...")
    for i, direction in enumerate(movements, 1):
        print(f"Step {i}: Moving {direction}")
        program.move_with_delay(direction)
    
    print("✅ Demo complete! The window will stay open for 10 seconds.")
    print("   You can see:")
    print("   • Blue triangle robot pointing east")
    print("   • Red trail showing movement path") 
    print("   • Black squares showing walls")
    
    time.sleep(10)
    print("🎓 Try creating your own robot programs!")
    print("   Check out: https://github.com/cherypallysaisurya/2d-Robot-dog-Simulation")
