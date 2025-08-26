"""High-level public API bridging simulator and hardware modes.

This file adapts logic from the previous minimal_api + controllers design.
"""
from __future__ import annotations
from typing import Optional
import time
import platform
import threading

from .controllers import build_program, Program


def create_robot_program(width: int = 10, height: int = 10, start_x: int = 0, start_y: int = 0,
                          mode: str = 'simulator', host: Optional[str] = None,
                          initial_mode: Optional[str] = 'Walk') -> Program:
    return build_program(width, height, start_x, start_y, mode=mode, host=host, initial_mode=initial_mode)


def run_with_visualization(program: Program, moves_function, move_delay: float = 1.5):
    """Execute student moves with visualization (sim) or timed playback (real)."""
    if getattr(program, 'mode', 'simulator') == 'real':
        print("🛠️ Real mode: running moves sequentially (no GUI)...")
        original_move = program.robot.move
        def move_with_delay(direction):
            result = original_move(direction)
            time.sleep(move_delay)
            return result
        program.robot.move = move_with_delay  # type: ignore
        try:
            moves_function()
        finally:
            program.robot.move = original_move
        print("✅ Real mode sequence complete.")
        return

    # Simulator path
    def enhanced_moves():
        time.sleep(1.5)
        original_move = program.robot.move
        from .core.robot import Position
        def move_with_notification(direction):
            old_pos = Position(program.robot.position.x, program.robot.position.y)
            success = original_move(direction)
            new_pos = program.robot.get_position()
            if hasattr(program, 'simulator') and program.simulator.running and getattr(program.simulator, 'canvas', None):
                program.simulator.robot_moved(old_pos, new_pos, success, move_delay)
                time.sleep(move_delay)
            return success
        program.robot.move = move_with_notification
        moves_function()
        program.robot.move = original_move

    if platform.system() == 'Darwin':
        enhanced_moves()
        program.start()
    else:
        thread = threading.Thread(target=enhanced_moves, daemon=True)
        thread.start()
        program.start()


def run_fast(program: Program, moves_function):
    run_with_visualization(program, moves_function, move_delay=0.5)

def run_normal(program: Program, moves_function):
    run_with_visualization(program, moves_function, move_delay=1.0)

def run_slow(program: Program, moves_function):
    run_with_visualization(program, moves_function, move_delay=2.5)

__all__ = [
    'create_robot_program',
    'run_with_visualization',
    'run_fast',
    'run_normal',
    'run_slow'
]
