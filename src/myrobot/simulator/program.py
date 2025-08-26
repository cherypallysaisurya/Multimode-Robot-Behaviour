"""Simulator program wrapper using the enhanced Tkinter visualization."""
from __future__ import annotations
from .visual import EnhancedSimulator
from ..core.robot import Robot, Position
import time

class RobotProgram:
    def __init__(self, width: int = 10, height: int = 10, start_x: int = 0, start_y: int = 0):
        self.robot = Robot(start_x, start_y)
        self.robot.grid_width = width
        self.robot.grid_height = height
        self.simulator = EnhancedSimulator(self.robot)
    def add_wall(self, x: int, y: int):
        self.robot.add_wall(x, y)
    def start(self):
        self.simulator.start_visualization()
    def move_with_delay(self, direction: str, delay: float = 1.5):
        old = Position(self.robot.position.x, self.robot.position.y)
        success = self.robot.move(direction)
        new = self.robot.get_position()
        if self.simulator.running:
            self.simulator.robot_moved(old, new, success, delay)
        time.sleep(delay)
        return success
