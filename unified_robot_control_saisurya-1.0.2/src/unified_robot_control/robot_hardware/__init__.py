"""
Real Robot Hardware Interface
============================

This module handles communication with real Go1 robot hardware.
Falls back gracefully when hardware is not available.
"""

from .go1_interface import Dog, Mode, MockDog, is_real_robot_available

__all__ = ["Dog", "Mode", "MockDog", "is_real_robot_available"]
