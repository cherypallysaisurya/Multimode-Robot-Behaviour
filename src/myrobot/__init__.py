"""myrobot unified educational robot package.

Public entrypoints:
- create_robot_program(...)
- run_with_visualization(program, moves_function, move_delay=1.5)

Environment variables:
- ROBOT_BEHAVIOR_HARDWARE_MOCK=1  Use in absence of real hardware.
"""
from .api import create_robot_program, run_with_visualization, run_fast, run_normal, run_slow

__all__ = [
    'create_robot_program',
    'run_with_visualization',
    'run_fast',
    'run_normal',
    'run_slow'
]
