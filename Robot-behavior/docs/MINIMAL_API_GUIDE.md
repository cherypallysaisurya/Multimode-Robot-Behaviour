# Minimal Robot API - Educational Documentation

## Overview

The Minimal Robot API is designed for educational programming, focusing on core movement concepts and forcing students to implement all complex logic themselves. The robot can only move in four fixed directions with strict obstacle detection.

## Core Philosophy

✅ **What the API Provides:**
- Basic directional movement: `move('up')`, `move('down')`, `move('left')`, `move('right')`, `move('backward')`
- Position checking: `get_position()`
- Maze loading: `load_maze(layout)`
- Obstacle detection with immediate simulation stopping
- Clear success/failure feedback

❌ **What Students Must Implement:**
- All pattern logic (spirals, prime numbers, etc.)
- Pathfinding and navigation algorithms
- Obstacle avoidance strategies
- Complex movement sequences
- Error handling and recovery

## Quick Start

```python
from robot_behavior.minimal_api import create_robot_program

# Create a robot program
program = create_robot_program(width=10, height=10, start_x=2, start_y=2)

# Basic movement
success = program.robot.move('right')
if success:
    print("Moved successfully!")
else:
    print("Move blocked - hit obstacle or boundary")

# Check position
pos = program.robot.get_position()
print(f"Robot is at: {pos}")

# Start visual simulator
program.start()
```

## Core API Reference

### Robot Movement

#### `robot.move(direction: str) -> bool`

Move robot one cell in specified direction.

**Parameters:**
- `direction`: One of `'up'`, `'down'`, `'left'`, `'right'`, `'backward'`

**Returns:**
- `True` if move successful
- `False` if blocked by obstacle or boundary

**Important:** Simulation stops immediately on failed moves. Students must handle this!

```python
# Example: Safe movement with error handling including backward
def safe_move(robot, direction):
    success = robot.move(direction)
    if not success:
        print(f"Cannot move {direction} - obstacle detected")
        # Student decides: reset, try different direction, etc.
    return success

# Backward movement - moves opposite to dog's facing direction
def move_backward_demo(robot):
    # Since dog faces EAST, backward moves WEST (left)
    robot.move('right')     # Move east (forward)
    robot.move('backward')  # Move west (backward)
```

#### `robot.get_position() -> Position`

Get current robot position.

**Returns:**
- `Position` object with `.x` and `.y` attributes

```python
pos = robot.get_position()
print(f"Robot at ({pos.x}, {pos.y})")
```

#### `robot.reset_simulation()`

Reset robot to starting position and clear simulation stop state.

```python
# After hitting obstacle, reset to continue
if robot.is_simulation_stopped():
    robot.reset_simulation()
    print("Robot reset - ready for new moves")
```

#### Understanding Backward Movement

The robot dog faces **EAST** (right direction). The `'backward'` command moves the robot in the **opposite direction** from where it's facing:

- **Forward direction**: `'right'` (east) - where the dog is facing
- **Backward direction**: `'backward'` (west) - opposite to where dog faces
- **Other directions**: `'up'` (north), `'down'` (south), `'left'` (west - same as backward)

```python
# Movement examples with east-facing dog
robot.move('right')     # Forward (east) ✅
robot.move('backward')  # Backward (west) ⬅️
robot.move('up')        # Up (north) ⬆️
robot.move('down')      # Down (south) ⬇️
robot.move('left')      # Left (west - same as backward) ⬅️
```

### Program Setup

#### `create_robot_program(width, height, start_x, start_y)`

Create new robot program with visual simulator.

```python
program = create_robot_program(
    width=12,     # Grid width
    height=8,     # Grid height  
    start_x=3,    # Starting X position
    start_y=2     # Starting Y position
)
```

#### `program.add_wall(x, y)`

Add obstacle at specified position.

```python
program.add_wall(5, 3)  # Wall at (5, 3)
program.add_wall(6, 3)  # Wall at (6, 3)
```

#### `program.load_maze(layout)`

Load maze from 2D layout.

**Maze Format:**
- `'.'` = empty space
- `'#'` = wall/obstacle  
- `'S'` = start position (optional)

```python
maze = [
    ['S', '.', '.', '#', '.'],
    ['.', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.']
]
program.load_maze(maze)
```

## Educational Examples

### 1. Prime Number Robot

Students implement prime checking and conditional movement:

```python
def student_prime_robot():
    program = create_robot_program(8, 6, 0, 0)
    
    # Student implements prime checking
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True
    
    # Student implements movement logic
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for num in numbers:
        if is_prime(num):
            success = program.robot.move('right')
            if not success:
                print("Hit obstacle!")
                break
        # Non-prime: stay in place
    
    program.start()
```

### 2. Maze Navigation

Students implement pathfinding algorithms:

```python
def student_maze_solver():
    program = create_robot_program()
    program.load_maze(SIMPLE_MAZE)
    
    # Student implements wall-following algorithm
    def try_directions(robot, order=['right', 'up', 'left', 'down']):
        for direction in order:
            if robot.move(direction):
                return True
        return False
    
    # Navigation loop
    for step in range(20):
        if not try_directions(program.robot):
            print("All directions blocked!")
            break
        program.update_display()
    
    program.start()
```

### 3. Spiral Pattern

Students implement algorithmic pattern generation:

```python
def student_spiral():
    program = create_robot_program(10, 10, 5, 5)
    
    # Student implements spiral logic
    directions = ['right', 'up', 'left', 'down']
    dir_index = 0
    steps_per_direction = 1
    steps_taken = 0
    
    for move in range(25):
        current_dir = directions[dir_index]
        
        if not program.robot.move(current_dir):
            break
            
        steps_taken += 1
        if steps_taken >= steps_per_direction:
            # Change direction and possibly increase steps
            dir_index = (dir_index + 1) % 4
            steps_taken = 0
            if dir_index % 2 == 0:  # Every 2 turns
                steps_per_direction += 1
        
        program.update_display()
    
    program.start()
```

## Debugging and Error Handling

### Move Logging

Check move history for debugging:

```python
# See all attempted moves
move_log = robot.get_move_log()
for move in move_log:
    print(f"Move {move['move_number']}: {move['direction']} - {move['success']}")
```

### Simulation State

Check if simulation stopped:

```python
if robot.is_simulation_stopped():
    print("Simulation stopped due to illegal move")
    # Options:
    robot.reset_simulation()  # Reset to start
    # OR fix movement logic and continue
```

### Position Validation

Students can implement their own boundary checking:

```python
def is_valid_position(robot, x, y):
    """Student implements position validation"""
    if x < 0 or x >= robot.grid_width:
        return False
    if y < 0 or y >= robot.grid_height:
        return False
    if (x, y) in robot.walls:
        return False
    return True

def safe_move_to(robot, target_x, target_y):
    """Student implements safe movement to target"""
    current = robot.get_position()
    
    # Calculate direction needed
    if target_x > current.x:
        direction = 'right'
    elif target_x < current.x:
        direction = 'left'
    elif target_y > current.y:
        direction = 'up'
    else:
        direction = 'down'
    
    # Validate before moving
    if is_valid_position(robot, target_x, target_y):
        return robot.move(direction)
    else:
        print(f"Cannot move to ({target_x}, {target_y}) - invalid position")
        return False
```

## Instructor Resources

### Creating Custom Mazes

```python
# Simple corridor maze
CORRIDOR_MAZE = [
    ['S', '.', '#', '.', '.'],
    ['.', '.', '#', '.', '.'],
    ['.', '.', '.', '.', '.']
]

# Complex maze with multiple paths
COMPLEX_MAZE = [
    ['S', '.', '#', '.', '.', '.', '.'],
    ['.', '.', '#', '.', '#', '#', '.'],
    ['#', '.', '#', '.', '.', '.', '.'],
    ['#', '.', '.', '.', '#', '.', '.'],
    ['.', '.', '#', '.', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.']
]
```

### Assignment Ideas

1. **Basic Movement**: Move robot in square pattern
2. **Prime Numbers**: Move only on prime number steps
3. **Maze Solving**: Navigate through instructor maze
4. **Obstacle Avoidance**: Create path around random obstacles
5. **Pattern Generation**: Create spiral, zigzag, or other patterns
6. **Pathfinding**: Implement A* or other search algorithms
7. **Creative Projects**: Temperature robot, treasure hunt, etc.

## Learning Objectives

Students will learn:

- **Basic Programming**: Variables, loops, conditionals
- **Algorithm Design**: Breaking problems into steps
- **Error Handling**: Dealing with failed operations
- **Debugging**: Using logs and systematic testing
- **Problem Solving**: Implementing solutions with limited tools
- **Mathematical Concepts**: Prime numbers, patterns, coordinates
- **Spatial Reasoning**: Grid navigation and positioning

## Key Differences from Advanced APIs

| Minimal API | Advanced APIs |
|-------------|---------------|
| Four fixed directions only | Rotation, angles, continuous movement |
| Immediate stop on illegal moves | Automatic obstacle avoidance |
| Students implement all logic | Built-in behavior patterns |
| Simple boolean success/failure | Complex movement animations |
| Focus on algorithmic thinking | Focus on using pre-built functions |

This minimal approach ensures students learn fundamental programming concepts rather than just calling pre-made functions.
