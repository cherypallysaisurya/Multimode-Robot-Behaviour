"""
Minimal Robot API for Educational Programming

This module provides the core robot movement API with strict obstacle detection.
Students must implement all complex behaviors using only these basic commands:

- robot.move(direction) - Move one cell in specified direction  
- robot.get_position() - Get current position
- robot.load_maze(layout) - Load instructor-defined maze
- robot.reset_simulation() - Reset after hitting obstacle

The simulation stops immediately on illegal moves, requiring students
to handle error cases and implement proper movement logic.
"""

from robot_behavior.core.robot import Robot, Position
from robot_behavior.simulator.enhanced_simulator import RobotProgram
from robot_behavior.controllers import build_program, Program  # new unified abstraction

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

def create_robot_program(width=10, height=10, start_x=0, start_y=0, mode: str = 'simulator', host: str | None = None):
    """Create a new program.

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
    # For compatibility with tests expecting a RobotProgram object *type*, we only
    # wrap with Program. Tests rely on program.robot.* so facade preserves access.
    return build_program(width, height, start_x, start_y, mode=mode, host=host)

def run_with_visualization(program, moves_function, move_delay=1.5):
    """
    Run student code with automatic real-time visualization.
    
    Args:
        program: Robot program created with create_robot_program()
        moves_function: Function containing robot moves
        move_delay: Delay in seconds between moves (default: 1.5)
        
    Example:
        program = create_robot_program(5, 5, 0, 1)
        def my_moves():
            program.robot.move('right')
            program.robot.move('up')
        run_with_visualization(program, my_moves, move_delay=2.0)  # Slower
        run_with_visualization(program, my_moves, move_delay=0.8)  # Faster
    """
    import threading
    import platform
    import time
    from robot_behavior.core.robot import Position
    
    def enhanced_moves():
        """Wrapper that adds simulator notifications to basic robot moves."""
        # Wait longer for GUI to fully initialize
        time.sleep(4.0)  # Increased wait time for GUI initialization
        
        # Wait until GUI is actually ready with better checking
        max_wait = 15  # Maximum 15 seconds
        wait_count = 0
        while (not hasattr(program, 'simulator') or 
               not program.simulator.running or 
               not hasattr(program.simulator, 'canvas') or 
               program.simulator.canvas is None) and wait_count < max_wait:
            time.sleep(0.5)
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
                time.sleep(move_delay)  # Customizable delay
            
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
