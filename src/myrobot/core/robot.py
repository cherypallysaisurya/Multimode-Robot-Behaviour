# Core robot logic copied from original project (trimmed docstring)
from enum import Enum
from typing import List, Dict, Any

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    BACKWARD = 'backward'

class Position:
    def __init__(self, x: int, y: int):
        self.x = x; self.y = y
    def __eq__(self, other): return self.x == other.x and self.y == other.y
    def __str__(self): return f"({self.x}, {self.y})"

class Robot:
    def __init__(self, start_x: int = 0, start_y: int = 0):
        self.start_position = Position(start_x, start_y)
        self.position = Position(start_x, start_y)
        self.grid_width = 10; self.grid_height = 10
        self.walls = set(); self.move_log = []; self._simulation_stopped = False
    def get_position(self) -> Position: return self.position
    def move(self, direction: str) -> bool:
        if self._simulation_stopped:
            print('❌ Simulation stopped.')
            return False
        try: dir_enum = Direction(direction.lower())
        except ValueError:
            print(f"❌ Invalid direction: {direction}.")
            self._simulation_stopped = True; return False
        new_x, new_y = self.position.x, self.position.y
        if dir_enum == Direction.UP: new_y += 1
        elif dir_enum == Direction.DOWN: new_y -= 1
        elif dir_enum == Direction.LEFT: new_x -= 1
        elif dir_enum == Direction.RIGHT: new_x += 1
        elif dir_enum == Direction.BACKWARD: new_x -= 1
        if new_x < 0 or new_x >= self.grid_width or new_y < 0 or new_y >= self.grid_height:
            print(f"❌ Move {direction} blocked: boundary")
            self._log_move(direction, False, 'boundary'); self._simulation_stopped = True; return False
        if (new_x, new_y) in self.walls:
            print(f"❌ Move {direction} blocked: obstacle")
            self._log_move(direction, False, 'obstacle'); self._simulation_stopped = True; return False
        old_pos = f"({self.position.x}, {self.position.y})"; self.position.x = new_x; self.position.y = new_y
        new_pos = f"({self.position.x}, {self.position.y})"; print(f"✅ Moved {direction}: {old_pos} → {new_pos}")
        self._log_move(direction, True, 'success'); return True
    def _log_move(self, direction: str, success: bool, reason: str):
        self.move_log.append({'direction': direction,'success': success,'reason': reason,'position_before': f"({self.position.x}, {self.position.y})",'move_number': len(self.move_log)+1})
    def reset_simulation(self):
        self.position = Position(self.start_position.x, self.start_position.y)
        self.move_log.clear(); self._simulation_stopped = False
        print(f"🔄 Robot reset to starting position: ({self.position.x}, {self.position.y})")
    def is_simulation_stopped(self) -> bool: return self._simulation_stopped
    def get_move_log(self) -> List[Dict[str, Any]]: return self.move_log.copy()
    def set_grid_size(self, width: int, height: int): self.grid_width = width; self.grid_height = height
    def add_wall(self, x: int, y: int):
        if (x, y) == (self.position.x, self.position.y): raise ValueError('Cannot place wall at robot position')
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height: self.walls.add((x, y))
    def load_maze(self, layout: List[List[str]]):
        if not layout or not layout[0]: return
        self.grid_height = len(layout); self.grid_width = len(layout[0]); self.walls.clear(); start_found = False
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                grid_y = self.grid_height - 1 - y
                if cell == '#': self.walls.add((x, grid_y))
                elif cell == 'S' and not start_found:
                    self.start_position = Position(x, grid_y); self.position = Position(x, grid_y); start_found = True
        if not start_found and (self.start_position.x, self.start_position.y) in self.walls:
            raise ValueError('Start inside wall')
        self._simulation_stopped = False; self.move_log.clear()

__all__ = ['Robot', 'Position']
