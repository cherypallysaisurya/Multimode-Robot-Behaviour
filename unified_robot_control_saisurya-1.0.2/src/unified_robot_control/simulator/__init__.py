"""
🤖 Robot Behavior Simulator - Educational Programming Framework

An engaging Python package that teaches programming concepts through visual robot simulation.
Perfect for beginners learning their first programming concepts!

🌟 Key Features:
- 🤖 Visual Robot: Circular icon that moves smoothly around a grid
- 🔴 Red Trail Visualization: See exactly where your robot has been
- 🧱 Obstacles & Walls: Navigate around barriers and solve maze challenges  
- ⚡ Immediate Feedback: Instant visual results help students understand their code
- 📚 Educational Focus: Designed specifically for teaching programming fundamentals

Quick Start:
    from unified_robot_control import create_robot_program
    
    # Create a 5x5 grid with robot starting at (0, 0)
    program = create_robot_program(5, 5, 0, 0)
    
    # Move the robot and watch the red trail appear!
    program.robot.move('right')
    program.robot.move('up')
    program.robot.move('backward')
    
    # Start the visual display
    program.start_with_auto_close(5)

Educational Concepts Taught:
- Sequential Programming: Execute commands in order
- Conditional Logic: Handle success/failure of movements
- Loops and Patterns: Create repeating behaviors
- Problem Solving: Navigate mazes and avoid obstacles
- Debugging: Use move logs and position checking

Perfect for educators teaching Python programming to beginners!
"""

# Core imports for main functionality
from .core.robot import Robot, Position, Direction
from .simulator.enhanced_simulator import RobotProgram, EnhancedSimulator
from .minimal_api import (
    create_robot_program,
    run_with_visualization,
    run_fast,
    run_slow,
    run_normal,
    load_maze_from_file,
    run_demo_example,
    SIMPLE_MAZE,
    STUDENT_MAZE
)

# Package metadata
__version__ = "1.0.3"
__author__ = "Robot Behavior Team" 
__email__ = "cherypallysaisurya@gmail.com"
__license__ = "MIT"
__description__ = "Educational robot simulation framework for teaching programming concepts"
__url__ = "https://github.com/cherypallysaisurya/2d-Robot-dog-Simulation"

# Main exports for easy importing
__all__ = [
    # Core classes
    'Robot',
    'Position',
    'Direction', 
    'RobotProgram',
    'EnhancedSimulator',
    
    # Main API functions
    'create_robot_program',
    'run_with_visualization',
    'run_fast',
    'run_slow', 
    'run_normal',
    'load_maze_from_file',
    'run_demo_example',
    
    # Maze layouts
    'SIMPLE_MAZE',
    'STUDENT_MAZE',
    
    # Package metadata
    '__version__',
    '__author__',
    '__license__',
]

# Version compatibility check
import sys
if sys.version_info < (3, 7):
    raise ImportError(
        f"robot_behavior requires Python 3.7 or later. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}"
    )

# Dependency checks with helpful error messages
try:
    import tkinter
except ImportError:
    raise ImportError(
        "robot_behavior requires tkinter for GUI functionality.\n"
        "Installation help:\n"
        "  Ubuntu/Debian: sudo apt install python3-tk\n"
        "  Fedora/CentOS: sudo dnf install python3-tkinter\n"
        "  macOS/Windows: tkinter included with Python"
    )

try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    raise ImportError(
        "robot_behavior requires Pillow for graphics.\n"
        "Install with: pip install Pillow>=8.0.0"
    )

# Interactive mode welcome message
def _show_interactive_help():
    """Show helpful message when imported interactively."""
    if hasattr(sys, 'ps1'):  # Check if in interactive mode
        print("🤖 Robot Behavior Simulator v{} loaded!".format(__version__))
        print("📚 Quick start: program = create_robot_program(5, 5, 0, 0)")
        print("🎮 Try demo: run_demo_example()")
        print("📖 Help: help(robot_behavior)")

_show_interactive_help()