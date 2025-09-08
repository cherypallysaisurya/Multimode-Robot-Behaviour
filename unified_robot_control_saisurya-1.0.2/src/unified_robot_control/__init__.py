"""
Unified Robot Control Library
============================

A unified educational robot control system supporting both 2D simulation 
and real Unitree Go1 quadruped robot with identical student API.

Students use simulator by default, TAs can switch to real robot via environment variables.
"""

from .core import create_robot_program, run_with_visualization

__version__ = "1.0.2"
__author__ = "Sai Surya"
__email__ = "csaisurya@example.com"

# Export main student-facing functions
__all__ = ["create_robot_program", "run_with_visualization"]
