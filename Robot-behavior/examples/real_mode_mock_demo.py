"""Demonstrate 'real' mode without hardware using the mock controller.

Run with:
    set ROBOT_BEHAVIOR_HARDWARE_MOCK=1   (Windows PowerShell)
    python real_mode_mock_demo.py

You should see logged mock actions instead of MQTT traffic.
"""

import os
os.environ.setdefault("ROBOT_BEHAVIOR_HARDWARE_MOCK", "1")  # force mock if not set

from robot_behavior.minimal_api import create_robot_program

program = create_robot_program(0, 0, 0, 0, mode="real")

for direction in ["up", "right", "down", "left", "up"]:
    program.robot.move(direction, speed=0.4, time=0.5)

print("Mock real mode sequence complete.")
print("(Set ROBOT_BEHAVIOR_HARDWARE_MOCK=0 to attempt real hardware connection.)")