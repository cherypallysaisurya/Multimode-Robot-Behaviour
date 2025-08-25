"""
Minimal Robot Behavior Framework for Educational Programming

This package provides a clean, minimal API for teaching programming concepts
through robot simulation. Students must implement all complex behaviors using
only basic movement commands.

Core Features:
- Four-direction movement with strict obstacle detection
- Immediate simulation stopping on illegal moves  
- Maze loading for instructor-designed challenges
- Clean visual feedback without distracting effects
- Comprehensive logging for debugging

Quick Start:
    from robot_behavior.minimal_api import create_robot_program
    
    program = create_robot_program(10, 10, 2, 2)
    program.robot.move('right')
    program.start()
"""

from .minimal_api import (
    Robot,
    Position, 
    RobotProgram,
    MinimalSimulator,
    create_robot_program,
    load_maze_from_file,
    SIMPLE_MAZE,
    STUDENT_MAZE
)

__version__ = "2.0.0"
__author__ = "Educational Robot Framework Team"

__all__ = [
    'Robot',
    'Position',
    'RobotProgram', 
    'MinimalSimulator',
    'create_robot_program',
    'load_maze_from_file',
    'SIMPLE_MAZE',
    'STUDENT_MAZE'
]
