"""Unified controllers and Program abstraction.

This module introduces a thin abstraction so the *same* student code
can target either the existing grid simulator ("simulator" mode) or a
real Go1 robot ("real" mode) backed by the MQTT Dog class from the
`go1_py` package.

Public Concepts
---------------
Program
    Container returned by create_robot_program(..., mode=...). It exposes
    a single `.robot` attribute whose interface is intentionally tiny:
        robot.move(direction: str, speed: float = 0.5, time: float = 1.0) -> bool
    (Only the *direction* is meaningful in simulator mode; speed/time
    are accepted for signature compatibility and ignored.)

Controllers
    SimulationController – wraps a grid Robot instance (existing implementation).
    Go1Controller – wraps a Dog (real robot). Directions map to Dog movement helpers.

Graceful error handling
-----------------------
Invalid directions return False and print a clear message instead of raising.

Lazy Hardware Import
--------------------
The real robot dependency (`go1_py`) is imported only when mode == "real"
so that simulation-only environments remain lightweight.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Callable, Any
import os

# Direction mapping accepted for both backends
VALID_DIRECTIONS = {"up", "down", "left", "right"}


class BaseController:
    """Common controller interface."""

    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:  # pragma: no cover - interface
        raise NotImplementedError


class SimulationController(BaseController):
    """Adapter over the existing grid Robot object."""

    def __init__(self, robot):
        self._robot = robot

    @property
    def robot(self):  # expose underlying for attribute delegation
        return self._robot

    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:  # noqa: D401
        # speed/time ignored for simulator; single-cell step semantics
        direction = direction.lower()
        if direction not in VALID_DIRECTIONS:
            print(f"❌ Invalid direction '{direction}'. Valid: {sorted(VALID_DIRECTIONS)}")
            return False
        return self._robot.move(direction)


class Go1Controller(BaseController):
    """Adapter wrapping a real Dog instance (from go1_py) or a mock.

    Mock mode
    ---------
    If the environment variable ``ROBOT_BEHAVIOR_HARDWARE_MOCK=1`` is set,
    a lightweight in‑memory fake Dog is used so developers without hardware
    can still exercise the unified real-mode pathway.
    """

    def __init__(self, host: Optional[str] = None):
        mock_enabled = os.getenv("ROBOT_BEHAVIOR_HARDWARE_MOCK") == "1"
        self._mock_log: list[str] = []

        if mock_enabled:
            class FakeDog:  # pragma: no cover - simple container
                def __init__(self, log: list[str]):
                    self._log = log
                def go_forward(self, speed, t): self._log.append(f"forward speed={speed} time={t}")
                def go_backward(self, speed, t): self._log.append(f"backward speed={speed} time={t}")
                def go_left(self, speed, t): self._log.append(f"left speed={speed} time={t}")
                def go_right(self, speed, t): self._log.append(f"right speed={speed} time={t}")
                def change_mode(self, mode): self._log.append(f"mode={mode}")
                def stop_moving(self): self._log.append("stop")
            self._dog = FakeDog(self._mock_log)
            print("🧪 Real mode mock enabled (ROBOT_BEHAVIOR_HARDWARE_MOCK=1) – no MQTT connection attempted.")
        else:
            try:
                from go1_py import Dog  # type: ignore
            except Exception as e:  # pragma: no cover - env dependent
                raise ImportError(
                    "go1_py package is required for real mode. Install extras: 'pip install robot-behavior-simulator[hardware]' or set ROBOT_BEHAVIOR_HARDWARE_MOCK=1 to mock."
                ) from e
            self._dog = Dog(host) if host else Dog()

        # Map directions to bound methods (closure capturing dog or fake dog)
        self._direction_map: dict[str, Callable[[float, float], Any]] = {
            "up": self._dog.go_forward,
            "down": self._dog.go_backward,
            "left": self._dog.go_left,
            "right": self._dog.go_right,
        }

    @property
    def dog(self):  # expose for advanced usage
        return self._dog

    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:
        direction = direction.lower()
        if direction not in VALID_DIRECTIONS:
            print(f"❌ Invalid direction '{direction}'. Valid: {sorted(VALID_DIRECTIONS)}")
            return False
        try:
            # Clamp speed between 0 and 1 for safety
            speed = max(0.0, min(1.0, speed))
            self._direction_map[direction](speed, time)
            return True
        except Exception as e:  # pragma: no cover - runtime safety
            print(f"⚠️ Move failed ({direction}): {e}")
            return False

    def mock_log(self) -> list[str]:  # expose captured log for tests when mocked
        return list(self._mock_log)


class UnifiedRobot:
    """Student-facing robot facade with a minimal uniform API.

    For simulator mode, attribute access falls back to the underlying grid
    robot so existing code (tests, examples) that rely on methods like
    get_position() continue to work.
    """

    def __init__(self, controller: BaseController, underlying_robot: Optional[object] = None):
        self._controller = controller
        self._underlying_robot = underlying_robot  # Only set for simulator

    def move(self, direction: str, speed: float = 0.5, time: float = 1.0) -> bool:
        return self._controller.move(direction, speed, time)

    def __getattr__(self, item):  # delegate for simulator compatibility
        if self._underlying_robot is not None and hasattr(self._underlying_robot, item):
            return getattr(self._underlying_robot, item)
        raise AttributeError(item)


class Program:
    """Unified Program abstraction.

    Attributes
    ----------
    robot : UnifiedRobot
        Facade exposing move(direction, speed=0.5, time=1.0) for both modes.
    mode : str
        'simulator' or 'real'.
    """

    def __init__(self, mode: str, inner_program: Optional[object] = None, controller: Optional[BaseController] = None):
        self.mode = mode
        self._inner = inner_program  # RobotProgram instance for simulator
        self._controller = controller
        underlying_robot = getattr(inner_program, 'robot', None) if inner_program else None
        self.robot = UnifiedRobot(controller, underlying_robot)

    # --- Simulator pass-through helpers (only meaningful in simulator mode) ---
    def add_wall(self, x: int, y: int):  # pragma: no cover - thin delegation
        if self.mode != 'simulator':
            print("ℹ️ add_wall ignored in real mode.")
            return
        return self._inner.add_wall(x, y)

    def start(self):  # pragma: no cover - GUI side-effect
        if self.mode != 'simulator':
            print("ℹ️ start() is simulator-only.")
            return
        return self._inner.start()

    def __getattr__(self, item):  # fallback to inner program for legacy API
        if self._inner and hasattr(self._inner, item):
            return getattr(self._inner, item)
        raise AttributeError(item)


def build_program(width: int, height: int, start_x: int, start_y: int, mode: str = 'simulator', host: str | None = None) -> Program:
    """Factory constructing a Program for the requested mode."""
    mode = (mode or 'simulator').lower()
    if mode == 'simulator':
        from robot_behavior.simulator.enhanced_simulator import RobotProgram  # local import
        inner = RobotProgram(width, height, start_x, start_y)
        controller = SimulationController(inner.robot)
        return Program(mode='simulator', inner_program=inner, controller=controller)
    elif mode == 'real':
        controller = Go1Controller(host=host)
        return Program(mode='real', inner_program=None, controller=controller)
    else:
        raise ValueError(f"Unsupported mode '{mode}'. Use 'simulator' or 'real'.")


__all__ = [
    'Program',
    'build_program',
    'SimulationController',
    'Go1Controller',
]
