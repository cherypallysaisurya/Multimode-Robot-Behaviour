"""
Go1 Robot Interface
==================

Unified interface for Go1 robot communication with graceful fallbacks.
"""

import os
import sys
from typing import Optional, Any

# Try to import real robot libraries
try:
    # Import from the bundled go1_py package
    from ..go1_py import Dog as _RealDog, Mode as _RealMode
    REAL_ROBOT_AVAILABLE = True
except ImportError:
    try:
        # Fallback: try system-installed go1_py
        from go1_py import Dog as _RealDog, Mode as _RealMode
        REAL_ROBOT_AVAILABLE = True
    except ImportError:
        _RealDog = None
        _RealMode = None
        REAL_ROBOT_AVAILABLE = False


class Mode:
    """Robot mode constants - works with or without real robot library."""
    
    def __init__(self):
        if REAL_ROBOT_AVAILABLE and _RealMode:
            # Use real modes if available
            self.Stand = getattr(_RealMode, 'Stand', 'Stand')
            self.Walk = getattr(_RealMode, 'Walk', 'Walk')
            self.Trot = getattr(_RealMode, 'Trot', 'Trot')
            self.Run = getattr(_RealMode, 'Run', 'Run')
        else:
            # Mock modes for development
            self.Stand = 'Stand'
            self.Walk = 'Walk'
            self.Trot = 'Trot'
            self.Run = 'Run'
    
    def __getattr__(self, name):
        """Dynamic attribute access for mode names."""
        if name.capitalize() in ['Stand', 'Walk', 'Trot', 'Run']:
            return name.capitalize()
        raise AttributeError(f"Mode has no attribute '{name}'")


# Global Mode instance
Mode = Mode()


class MockDog:
    """Mock robot for development and testing."""
    
    def __init__(self, host: str):
        self.host = host
        self.log = []
        print(f"🧪 MOCK Robot initialized (simulated connection to {host})")
    
    def go_forward(self, speed: float, time: float):
        self.log.append(f"go_forward(speed={speed}, time={time})")
        print(f"🤖 MOCK: Moving forward (speed={speed:.2f}, time={time:.2f}s)")
    
    def go_backward(self, speed: float, time: float):
        self.log.append(f"go_backward(speed={speed}, time={time})")
        print(f"🤖 MOCK: Moving backward (speed={speed:.2f}, time={time:.2f}s)")
    
    def go_left(self, speed: float, time: float):
        self.log.append(f"go_left(speed={speed}, time={time})")
        print(f"🤖 MOCK: Moving left (speed={speed:.2f}, time={time:.2f}s)")
    
    def go_right(self, speed: float, time: float):
        self.log.append(f"go_right(speed={speed}, time={time})")
        print(f"🤖 MOCK: Moving right (speed={speed:.2f}, time={time:.2f}s)")
    
    def change_mode(self, mode: Any):
        self.log.append(f"change_mode({mode})")
        print(f"🤖 MOCK: Changed mode to {mode}")
    
    def get_log(self):
        """Return command log for debugging."""
        return self.log.copy()


class Dog:
    """
    Unified Dog interface that works with real robot or falls back to mock.
    """
    
    def __init__(self, host: str, use_mock: bool = False):
        self.host = host
        self._is_mock = use_mock or not REAL_ROBOT_AVAILABLE
        self._robot = None
        
        if self._is_mock or not REAL_ROBOT_AVAILABLE:
            self._setup_mock()
        else:
            self._setup_real_robot()
    
    def _setup_mock(self):
        """Initialize mock robot."""
        self._robot = MockDog(self.host)
        self._is_mock = True
    
    def _setup_real_robot(self):
        """Initialize real robot with error handling."""
        try:
            # Test network connectivity first
            import socket
            socket.setdefaulttimeout(3)
            
            # Try to create socket connection to test reachability
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex((self.host, 1001))  # Common robot port
                if result != 0:
                    print(f"⚠️  Cannot reach robot at {self.host}, using mock mode")
                    self._setup_mock()
                    return
            
            # Create real robot connection
            self._robot = _RealDog(self.host)
            print(f"🤖 Real robot connected at {self.host}")
            
        except Exception as e:
            print(f"⚠️  Real robot connection failed: {e}")
            print("🧪 Falling back to mock mode")
            self._setup_mock()
    
    def go_forward(self, speed: float, time: float):
        """Move robot forward."""
        return self._robot.go_forward(speed, time)
    
    def go_backward(self, speed: float, time: float):
        """Move robot backward.""" 
        return self._robot.go_backward(speed, time)
    
    def go_left(self, speed: float, time: float):
        """Move robot left."""
        return self._robot.go_left(speed, time)
    
    def go_right(self, speed: float, time: float):
        """Move robot right."""
        return self._robot.go_right(speed, time)
    
    def change_mode(self, mode: Any):
        """Change robot locomotion mode."""
        return self._robot.change_mode(mode)
    
    @property
    def is_mock(self) -> bool:
        """Check if using mock robot."""
        return self._is_mock
    
    def get_log(self):
        """Get command log (mock only)."""
        if hasattr(self._robot, 'get_log'):
            return self._robot.get_log()
        return []


def test_robot_connection(host: str = "192.168.12.1") -> bool:
    """
    Test if real robot is available.
    
    Args:
        host: Robot IP address
        
    Returns:
        bool: True if real robot is available
    """
    if not REAL_ROBOT_AVAILABLE:
        return False
        
    try:
        import socket
        socket.setdefaulttimeout(2)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((host, 1001))
            return result == 0
    except:
        return False


# Convenience function for checking robot availability
def is_real_robot_available(host: str = "192.168.12.1") -> bool:
    """Check if real robot hardware is available."""
    return REAL_ROBOT_AVAILABLE and test_robot_connection(host)
