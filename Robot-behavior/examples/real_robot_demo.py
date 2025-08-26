"""Real Unitree Go1 demo using the unified student API.

Prerequisites:
  pip install .[hardware]
  Robot reachable at default hostname 'go1-max' or pass host=...

Safety: Clear area, start in Stand or Walk. Adjust speed/time conservatively.
"""
from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def main():
    program = create_robot_program(5, 5, 0, 0, mode="real", initial_mode="Walk")

    def moves():
        # Simple pattern (lateral right, then forward). Adjust as needed.
        program.robot.move('right', speed=0.3, time=0.8)
        program.robot.move('right', speed=0.3, time=0.8)
        program.robot.move('up',    speed=0.4, time=1.0)
        program.robot.move('right', speed=0.3, time=0.8)
        program.robot.move('up',    speed=0.4, time=1.0)

    run_with_visualization(program, moves, move_delay=0.8)

if __name__ == '__main__':
    main()
