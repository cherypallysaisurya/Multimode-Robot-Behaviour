
import os

# Environment variable override (for TAs)
# Students use mode parameter normally, TAs can set ROBOT_MODE=real
MODE = os.getenv("ROBOT_MODE", "simulator").lower()  # Default to simulator


ROBOT_SETTINGS = {
    "host": "192.168.12.1",      #
    "initial_mode": "walk",      # Starting robot mode (lowercase)
    "move_speed": 0.3,           # Movement speed (0.0 to 1.0)
    "move_time": 1.0,            # Duration of each move in seconds
    "turn_speed": 0.3,           # Turning speed (0.0 to 1.0)
    "turn_time": 1.0,            # Duration of each turn in seconds
}


SIMULATOR_SETTINGS = {
    "grid_width": 8,
    "grid_height": 8,
    "start_x": 0,
    "start_y": 0,
    "visualization_delay": 0.5,  
}


class RobotInterface:
   
    
    def __init__(self, mode: str):
        self.mode = mode.lower()
        self._backend = None
        self._setup_backend()
    
    def _setup_backend(self):
        
        if self.mode == "simulator":
            self._setup_simulator()
        elif self.mode == "real":
            self._setup_real_robot()
        else:
            raise ValueError(f"Unknown mode: {self.mode}. Use 'simulator' or 'real'")
    
    def _setup_simulator(self):
        
        try:
            
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Robot-behavior'))
            from robot_behavior import create_robot_program
            
            self._backend = create_robot_program(
                SIMULATOR_SETTINGS["grid_width"],
                SIMULATOR_SETTINGS["grid_height"], 
                SIMULATOR_SETTINGS["start_x"],
                SIMULATOR_SETTINGS["start_y"],
                mode="simulator"
            )
            print("🎮 Simulator mode initialized")
            
        except ImportError as e:
            print(f"❌ Failed to initialize simulator: {e}")
            raise
    
    def _setup_real_robot(self):
        """Setup real robot backend"""
        try:
            from go1_py import Dog, Mode
            
            print("🔄 Connecting to robot...")
            import socket
            socket.setdefaulttimeout(3)  # 3 second timeout
            
            self._dog = Dog(ROBOT_SETTINGS["host"])
            
            # Safe initialization sequence
            print("🔄 Robot initialization sequence:")
            print("   1. Ensuring robot is standing...")
            self._dog.change_mode(Mode.Stand)
            
            print("   2. Waiting for stable position...")
            import time
            time.sleep(2)  # Give robot time to stabilize
            
            print("   3. Transitioning to movement mode...")
            mode_name = ROBOT_SETTINGS["initial_mode"]
            initial_mode = getattr(Mode, mode_name.capitalize())
            self._dog.change_mode(initial_mode)
            
            print("   4. Ready for movement commands!")
            print(f"🤖 Real robot initialized (host: {ROBOT_SETTINGS['host']}, mode: {mode_name})")
            
        except Exception as e:
            print(f"🧪 Real robot not available - using mock mode")
            self._setup_mock_robot()
    
    def _setup_mock_robot(self):

        class MockDog:
            def __init__(self, host):
                self.host = host
                self.log = []
            
            def go_forward(self, speed, time):
                self.log.append(f"MOCK: go_forward(speed={speed}, time={time})")
                print(f"🤖 MOCK: Moving forward (speed={speed}, time={time})")
            
            def go_backward(self, speed, time):
                self.log.append(f"MOCK: go_backward(speed={speed}, time={time})")
                print(f"🤖 MOCK: Moving backward (speed={speed}, time={time})")
            
            def go_left(self, speed, time):
                self.log.append(f"MOCK: go_left(speed={speed}, time={time})")
                print(f"🤖 MOCK: Moving left (speed={speed}, time={time})")
            
            def go_right(self, speed, time):
                self.log.append(f"MOCK: go_right(speed={speed}, time={time})")
                print(f"🤖 MOCK: Moving right (speed={speed}, time={time})")
            
            def change_mode(self, mode):
                self.log.append(f"MOCK: change_mode({mode})")
                print(f"🤖 MOCK: Changed mode to {mode}")
        
        self._dog = MockDog(ROBOT_SETTINGS["host"])
        self._dog.change_mode(ROBOT_SETTINGS["initial_mode"])
    
    def move(self, direction: str) -> bool:
        direction = direction.lower().strip()
        
        if self.mode == "simulator":
            return self._move_simulator(direction)
        elif self.mode == "real":
            return self._move_real_robot(direction)
        
        return False
    
    def _move_simulator(self, direction: str) -> bool:
        
        try:
            return self._backend.robot.move(direction)
        except Exception as e:
            print(f"❌ Simulator move failed: {e}")
            return False
    
    def _move_real_robot(self, direction: str) -> bool:
        """Handle real robot movement"""
        try:
            
            speed, time = self._get_movement_params(direction)
            
            if direction == "up":
                self._dog.go_forward(speed, time)
            elif direction == "down": 
                self._dog.go_backward(speed, time)
            elif direction == "left":
                self._dog.go_left(speed, time)
            elif direction == "right":
                self._dog.go_right(speed, time)
            else:
                print(f"❌ Invalid direction: {direction}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Real robot move failed: {e}")
            return False
    
    def _get_movement_params(self, direction: str) -> tuple[float, float]:
        """
        Get speed and time parameters for movement.
        Programmer can modify this to adjust robot behavior.
        """
        if direction in ["left", "right"]:
            return ROBOT_SETTINGS["turn_speed"], ROBOT_SETTINGS["turn_time"]
        else:  # up, down
            return ROBOT_SETTINGS["move_speed"], ROBOT_SETTINGS["move_time"]
    
    def add_wall(self, x: int, y: int):
        """Add wall (simulator only) - for compatibility"""
        if self.mode == "simulator":
            self._backend.add_wall(x, y)
        else:
            print("ℹ️ add_wall ignored in real robot mode")
    
    def start_visualization(self):
        """Start visualization (simulator only)"""
        if self.mode == "simulator":
            self._backend.start()
        else:
            print("ℹ️ Visualization not available in real robot mode")


class RobotProgram:
    """
    Simple wrapper that students interact with.
    Provides the familiar program.robot.move() interface.
    """
    
    def __init__(self, mode: str = None):
        if mode is None:
            mode = MODE  # Use global setting
        self.robot = RobotInterface(mode)
        self.mode = mode
    
    def add_wall(self, x: int, y: int):
        """Add wall (simulator only)"""
        self.robot.add_wall(x, y)
    
    def start(self):
        """Start visualization (simulator only)"""
        self.robot.start_visualization()



def create_robot_program(grid_width=None, grid_height=None, start_x=None, start_y=None, mode=None) -> RobotProgram:
    """
    Create a robot program that students can use.
    
    Args:
        grid_width: Width of simulator grid (default: 8)
        grid_height: Height of simulator grid (default: 8)
        start_x: Starting X position (default: 0)
        start_y: Starting Y position (default: 0)
        mode: "simulator" or "real" (default: uses environment or "simulator")
    
    Returns:
        RobotProgram: Program with robot.move() interface
    
    Example student usage:
        # Normal usage (simulator by default)
        program = create_robot_program()
        
        # Custom grid size
        program = create_robot_program(grid_width=10, grid_height=6)
        
        # Force mode (students can still do this)
        program = create_robot_program(mode="real")
        
        # TAs can override with environment: export ROBOT_MODE=real
    """
    # Priority: explicit mode > environment variable > default simulator
    if mode is not None:
        current_mode = mode
    else:
        current_mode = MODE  # Uses environment variable or default
    
    # Update simulator settings for this specific program instance
    if current_mode == "simulator" and any(param is not None for param in [grid_width, grid_height, start_x, start_y]):
        # Create temporary settings for this instance
        temp_settings = SIMULATOR_SETTINGS.copy()
        if grid_width is not None:
            temp_settings["grid_width"] = grid_width
        if grid_height is not None:
            temp_settings["grid_height"] = grid_height
        if start_x is not None:
            temp_settings["start_x"] = start_x
        if start_y is not None:
            temp_settings["start_y"] = start_y
        
        # Store original settings
        original_settings = SIMULATOR_SETTINGS.copy()
        
        # Temporarily update global settings
        SIMULATOR_SETTINGS.update(temp_settings)
        
        try:
            program = RobotProgram(current_mode)
            # Store custom settings with the program for later use
            program._custom_settings = temp_settings
        finally:
            # Restore original settings
            SIMULATOR_SETTINGS.update(original_settings)
    else:
        program = RobotProgram(current_mode)
        program._custom_settings = None
    
    return program


def run_with_visualization(program: RobotProgram, moves_function, move_delay: float = None):
    """
    Run student moves with appropriate visualization/delay.
    
    Args:
        program: Robot program created with create_robot_program()
        moves_function: Function containing student's robot.move() calls
        move_delay: Optional delay override
    """
    if move_delay is None:
        move_delay = SIMULATOR_SETTINGS["visualization_delay"]
    
    if program.mode == "simulator":
        # Use existing visualization system
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Robot-behavior'))
            from robot_behavior import run_with_visualization as sim_viz
            sim_viz(program.robot._backend, moves_function, move_delay)
        except ImportError:
            print("❌ Simulator visualization not available, running moves only")
            moves_function()
    else:
        # Real robot: just run moves with delays
        import time
        print("🛠️ Real robot mode: executing moves...")
        
        original_move = program.robot.move
        def move_with_delay(direction):
            result = original_move(direction)
            time.sleep(move_delay)
            return result
        
        program.robot.move = move_with_delay
        try:
            moves_function()
        finally:
            program.robot.move = original_move
        
        print("✅ Move sequence complete")


# Export the student-facing functions
__all__ = ["create_robot_program", "run_with_visualization"]
