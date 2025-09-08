from enum import Enum
from typing import Tuple, Dict, Any, List

class Direction(Enum):
    UP = "up"
    DOWN = "down" 
    LEFT = "left"
    RIGHT = "right"
    BACKWARD = "backward"  # Move in opposite direction (west, since dog faces east)

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

class Robot:
    """
    Minimal Robot API for educational purposes.
    
    This robot can only move in four fixed directions and provides
    strict obstacle detection. Students must implement all complex
    behaviors using only these basic movement commands.
    """
    
    def __init__(self, start_x: int = 0, start_y: int = 0):
        self.start_position = Position(start_x, start_y)
        self.position = Position(start_x, start_y)
        self.grid_width = 10
        self.grid_height = 10
        self.walls = set()
        self.move_log = []
        self._simulation_stopped = False
    
    def get_position(self) -> Position:
        """Get current robot position."""
        return self.position
    
    def move(self, direction: str) -> bool:
        """
        Move robot one cell in the specified direction.
        
        Args:
            direction: One of 'up', 'down', 'left', 'right'
            
        Returns:
            bool: True if move successful, False if blocked or invalid
            
        Note: If move fails, robot position remains unchanged.
        Simulation stops on illegal moves - students must handle this.
        """
        if self._simulation_stopped:
            print("❌ Simulation stopped. Reset or fix movement logic.")
            return False
            
        # Validate direction
        try:
            dir_enum = Direction(direction.lower())
        except ValueError:
            print(f"❌ Invalid direction: {direction}. Use: up, down, left, right, backward")
            self._simulation_stopped = True
            return False
        
        # Calculate new position
        new_x, new_y = self.position.x, self.position.y
        
        if dir_enum == Direction.UP:
            new_y += 1
        elif dir_enum == Direction.DOWN:
            new_y -= 1
        elif dir_enum == Direction.LEFT:
            new_x -= 1
        elif dir_enum == Direction.RIGHT:
            new_x += 1
        elif dir_enum == Direction.BACKWARD:
            # Since dog faces east, backward means move west (left)
            new_x -= 1
        
        # Check boundaries
        if new_x < 0 or new_x >= self.grid_width or new_y < 0 or new_y >= self.grid_height:
            print(f"❌ Move {direction} blocked: boundary hit at ({new_x}, {new_y})")
            self._log_move(direction, False, "boundary")
            self._simulation_stopped = True
            return False
        
        # Check walls/obstacles
        if (new_x, new_y) in self.walls:
            print(f"❌ Move {direction} blocked: obstacle at ({new_x}, {new_y})")
            self._log_move(direction, False, "obstacle")
            self._simulation_stopped = True
            return False
        
        # Move is valid - update position
        old_pos = f"({self.position.x}, {self.position.y})"
        self.position.x = new_x
        self.position.y = new_y
        new_pos = f"({self.position.x}, {self.position.y})"
        
        print(f"✅ Moved {direction}: {old_pos} → {new_pos}")
        self._log_move(direction, True, "success")
        return True
    
    def _log_move(self, direction: str, success: bool, reason: str):
        """Log move attempt for debugging purposes."""
        self.move_log.append({
            'direction': direction,
            'success': success,
            'reason': reason,
            'position_before': f"({self.position.x}, {self.position.y})",
            'move_number': len(self.move_log) + 1
        })
    
    def reset_simulation(self):
        """Reset robot to starting position and clear simulation stop."""
        self.position = Position(self.start_position.x, self.start_position.y)
        self.move_log.clear()
        self._simulation_stopped = False
        print(f"🔄 Robot reset to starting position: ({self.position.x}, {self.position.y})")
    
    def is_simulation_stopped(self) -> bool:
        """Check if simulation is stopped due to illegal move."""
        return self._simulation_stopped
    
    def get_move_log(self) -> List[Dict[str, Any]]:
        """Get log of all move attempts for debugging."""
        return self.move_log.copy()
    
    def set_grid_size(self, width: int, height: int):
        """Set the grid boundaries."""
        self.grid_width = width
        self.grid_height = height
        print(f"📐 Grid size set to {width} x {height}")
    
    def add_wall(self, x: int, y: int):
        """Add a wall/obstacle at the specified position."""
        # Prevent adding a wall where the robot currently starts or stands
        if (x, y) == (self.position.x, self.position.y):
            raise ValueError(f"Cannot place wall at robot position/start ({x}, {y})")

        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            if (x, y) in self.walls:
                print(f"⚠️ Wall already exists at ({x}, {y})")
            else:
                self.walls.add((x, y))
                print(f"🧱 Wall added at ({x}, {y})")
        else:
            print(f"❌ Cannot add wall at ({x}, {y}) - outside grid boundaries")
    
    def load_maze(self, layout: List[List[str]]):
        """
        Load a maze layout where:
        '.' = empty space
        '#' = wall/obstacle
        'S' = start position (optional)
        
        Args:
            layout: 2D list representing the maze
        """
        if not layout or not layout[0]:
            print("❌ Invalid maze layout")
            return
            
        self.grid_height = len(layout)
        self.grid_width = len(layout[0])
        self.walls.clear()
        
        # Find start position and walls
        start_found = False
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                # Convert to our coordinate system (y=0 at bottom)
                grid_y = self.grid_height - 1 - y
                
                if cell == '#':
                    self.walls.add((x, grid_y))
                elif cell == 'S' and not start_found:
                    self.start_position = Position(x, grid_y)
                    self.position = Position(x, grid_y)
                    start_found = True

        # If start marker not provided, ensure start position not inside a wall
        if not start_found and (self.start_position.x, self.start_position.y) in self.walls:
            raise ValueError(f"Robot start position ({self.start_position.x}, {self.start_position.y}) is inside a wall in the maze definition")
        
        self._simulation_stopped = False
        self.move_log.clear()
        
        print(f"🗺️ Maze loaded: {self.grid_width}x{self.grid_height} with {len(self.walls)} walls")
        print(f"🤖 Robot positioned at: ({self.position.x}, {self.position.y})")
    
    def set_simulator(self, simulator):
        """Set the simulator instance for this robot."""
        self.simulator = simulator
    
    def is_simulation_stopped(self) -> bool:
        """Check if simulation has been stopped due to collision."""
        return self._simulation_stopped
