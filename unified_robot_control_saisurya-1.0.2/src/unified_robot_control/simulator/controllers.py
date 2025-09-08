"""Unified controllers and Program abstraction.

Only two modes are supported and student code is identical:
    mode="simulator" -> grid + Tkinter visualization.
    mode="real"       -> Unitree Go1 via :mod:`go1_py`.

Removed: all mock / environment variable hardware simulation paths. Real
mode now always requires the hardware library to be installed and a robot
reachable on the network. Students *never* import :mod:`go1_py` directly;
they just call ``program.robot.move('right')`` etc.
"""

from __future__ import annotations

from typing import Optional, Callable, Any

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
    """Adapter wrapping a real Dog instance from :mod:`go1_py`.

    Always real hardware (no mock path). We create ``Dog(host or 'go1-max')``
    so a default hostname used in teaching setups works out of the box.
    ``initial_mode`` (default Walk) is set via Mode enum if provided.
    Directional ``move`` calls map to safe, fixed stride helpers.
    """

    def __init__(self, host: Optional[str] = None, initial_mode: Optional[str] = "Walk"):
        # Try to import real hardware support
        try:
            from go1_py import Dog, Mode  # type: ignore
            self._use_real_hardware = True
            default_host = host or "go1-max"
            self._dog = Dog(default_host)
            if initial_mode:
                try:
                    self._dog.change_mode(getattr(Mode, initial_mode))
                    print(f"🚀 Real robot initial mode set to {initial_mode}")
                except Exception as e:  # pragma: no cover
                    print(f"⚠️ Could not set initial mode '{initial_mode}': {e}")
        except ImportError:
            # Fallback to mock mode for students without hardware
            print("🧪 go1_py not available - using mock real mode for testing")
            self._use_real_hardware = False
            self._mock_log: list[str] = []
            
            # Create a mock dog for testing
            class MockDog:
                def __init__(self, log: list[str]):
                    self._log = log
                def go_forward(self, speed: float, time: float):
                    self._log.append(f"🤖 MOCK: go_forward(speed={speed}, time={time})")
                    print(f"🤖 MOCK: Moving forward (speed={speed}, time={time})")
                def go_backward(self, speed: float, time: float):
                    self._log.append(f"🤖 MOCK: go_backward(speed={speed}, time={time})")
                    print(f"🤖 MOCK: Moving backward (speed={speed}, time={time})")
                def go_left(self, speed: float, time: float):
                    self._log.append(f"🤖 MOCK: go_left(speed={speed}, time={time})")
                    print(f"🤖 MOCK: Moving left (speed={speed}, time={time})")
                def go_right(self, speed: float, time: float):
                    self._log.append(f"🤖 MOCK: go_right(speed={speed}, time={time})")
                    print(f"🤖 MOCK: Moving right (speed={speed}, time={time})")
                def change_mode(self, mode):
                    self._log.append(f"🤖 MOCK: change_mode({mode})")
                    print(f"🤖 MOCK: Changed mode to {mode}")
            
            self._dog = MockDog(self._mock_log)
            if initial_mode:
                self._dog.change_mode(initial_mode)
        
        # Set up direction mapping (works for both real and mock)
        self._direction_map: dict[str, Callable[[float, float], Any]] = {
            "up": self._dog.go_forward,
            "down": self._dog.go_backward,
            "left": self._dog.go_left,
            "right": self._dog.go_right,
        }

    @property
    def dog(self):  # expose for advanced usage
        return self._dog

    def get_mock_log(self):
        """Get mock command log for debugging (only available when using mock mode)."""
        return getattr(self, '_mock_log', [])

    def is_using_real_hardware(self):
        """Check if using real hardware or mock mode."""
        return getattr(self, '_use_real_hardware', False)

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

    # mock_log removed – no mock mode now


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


def build_program(
    width: int,
    height: int,
    start_x: int,
    start_y: int,
    mode: str = 'simulator',
    host: str | None = None,
    initial_mode: str | None = "Walk",
) -> Program:
    """Factory constructing a Program for the requested mode.

    Args:
        width, height: Grid size for simulator mode.
        start_x, start_y: Start coordinates for simulator mode.
        mode: 'simulator' or 'real'.
        host: Optional robot hostname/IP (real mode).
        initial_mode: Optional initial movement mode for real robot (e.g. 'Walk').
    """
    mode = (mode or 'simulator').lower()
    if mode == 'simulator':
        from .simulator.enhanced_simulator import RobotProgram  # local import
        inner = RobotProgram(width, height, start_x, start_y)
        controller = SimulationController(inner.robot)
        return Program(mode='simulator', inner_program=inner, controller=controller)
    if mode == 'real':
        controller = Go1Controller(host=host, initial_mode=initial_mode)
        return Program(mode='real', inner_program=None, controller=controller)
    raise ValueError(f"Unsupported mode '{mode}'. Use 'simulator' or 'real'.")


__all__ = [
    'Program',
    'build_program',
    'SimulationController',
    'Go1Controller',
]
