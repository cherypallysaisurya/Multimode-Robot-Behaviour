# Controllers adapted from original project (simplified import paths)
from __future__ import annotations
from typing import Optional, Callable, Any
import os

VALID_DIRECTIONS = {"up", "down", "left", "right"}

class BaseController:
    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:  # pragma: no cover
        raise NotImplementedError

class SimulationController(BaseController):
    def __init__(self, robot):
        self._robot = robot
    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:
        d = direction.lower()
        if d not in VALID_DIRECTIONS:
            print(f"❌ Invalid direction '{direction}'. Valid: {sorted(VALID_DIRECTIONS)}")
            return False
        return self._robot.move(d)

class Go1Controller(BaseController):
    def __init__(self, host: Optional[str] = None, initial_mode: Optional[str] = 'Walk'):
        mock_enabled = os.getenv('ROBOT_BEHAVIOR_HARDWARE_MOCK') == '1'
        self._mock_log: list[str] = []
        if mock_enabled:
            class FakeDog:
                def __init__(self, log: list[str]): self._log = log
                def go_forward(self, s, t): self._log.append(f"forward s={s} t={t}")
                def go_backward(self, s, t): self._log.append(f"backward s={s} t={t}")
                def go_left(self, s, t): self._log.append(f"left s={s} t={t}")
                def go_right(self, s, t): self._log.append(f"right s={s} t={t}")
                def change_mode(self, m): self._log.append(f"mode={m}")
            self._dog = FakeDog(self._mock_log)
            print("🧪 Mock real mode enabled (no MQTT).")
        else:
            from go1_py import Dog  # type: ignore
            self._dog = Dog(host) if host else Dog()
        if initial_mode:
            try:
                if mock_enabled:
                    self._dog.change_mode(initial_mode)
                else:
                    from go1_py import Mode  # type: ignore
                    self._dog.change_mode(getattr(Mode, initial_mode))
                print(f"🚀 Initial mode set to {initial_mode}")
            except Exception as e:
                print(f"⚠️ Could not set initial mode '{initial_mode}': {e}")
        self._direction_map: dict[str, Callable[[float, float], Any]] = {
            'up': self._dog.go_forward,
            'down': self._dog.go_backward,
            'left': self._dog.go_left,
            'right': self._dog.go_right,
        }
    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:
        d = direction.lower()
        if d not in VALID_DIRECTIONS:
            print(f"❌ Invalid direction '{direction}'. Valid: {sorted(VALID_DIRECTIONS)}")
            return False
        try:
            speed = max(0.0, min(1.0, speed))
            self._direction_map[d](speed, time)
            return True
        except Exception as e:
            print(f"⚠️ Move failed ({d}): {e}")
            return False
    def mock_log(self):
        return list(self._mock_log)

class UnifiedRobot:
    def __init__(self, controller: BaseController, underlying_robot=None):
        self._controller = controller
        self._underlying = underlying_robot
    def move(self, direction: str, speed: float = 0.5, time: float = 1.0):
        return self._controller.move(direction, speed, time)
    def __getattr__(self, item):
        if self._underlying is not None and hasattr(self._underlying, item):
            return getattr(self._underlying, item)
        raise AttributeError(item)

class Program:
    def __init__(self, mode: str, inner_program=None, controller: BaseController | None = None):
        self.mode = mode
        self._inner = inner_program
        self._controller = controller
        underlying = getattr(inner_program, 'robot', None) if inner_program else None
        self.robot = UnifiedRobot(controller, underlying)
    def add_wall(self, x: int, y: int):
        if self.mode != 'simulator':
            print('ℹ️ add_wall ignored in real mode.')
            return
        return self._inner.add_wall(x, y)
    def start(self):
        if self.mode != 'simulator':
            print('ℹ️ start() simulator only.')
            return
        return self._inner.start()
    def __getattr__(self, item):
        if self._inner and hasattr(self._inner, item):
            return getattr(self._inner, item)
        raise AttributeError(item)

# Build program

def build_program(width: int, height: int, start_x: int, start_y: int, mode: str = 'simulator', host: str | None = None, initial_mode: str | None = 'Walk') -> Program:
    m = (mode or 'simulator').lower()
    if m == 'simulator':
        from .simulator.program import RobotProgram
        inner = RobotProgram(width, height, start_x, start_y)
        controller = SimulationController(inner.robot)
        return Program('simulator', inner, controller)
    if m == 'real':
        controller = Go1Controller(host=host, initial_mode=initial_mode)
        return Program('real', None, controller)
    raise ValueError(f"Unsupported mode '{mode}'.")

__all__ = ['Program', 'build_program', 'Go1Controller', 'SimulationController']
