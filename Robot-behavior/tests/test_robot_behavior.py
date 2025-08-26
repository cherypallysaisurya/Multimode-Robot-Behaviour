#!/usr/bin/env python3
"""
Comprehensive tests for robot-behavior-simulator package.
Tests core functionality without GUI dependencies.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from robot_behavior.minimal_api import create_robot_program, SIMPLE_MAZE, STUDENT_MAZE
from robot_behavior.core.robot import Robot, Position, Direction


class TestRobotBasics:
    """Test basic robot functionality."""
    
    def test_robot_creation(self):
        """Test that robot can be created with default parameters."""
        robot = Robot(0, 0)
        assert robot.get_position().x == 0
        assert robot.get_position().y == 0
        assert robot.grid_width == 10
        assert robot.grid_height == 10
        assert robot.is_simulation_stopped() == False
    
    def test_robot_movement_success(self):
        """Test successful robot movement in all directions."""
        robot = Robot(2, 2)  # Start in middle to allow all movements
        robot.set_grid_size(5, 5)
        
        # Test right movement
        success = robot.move('right')
        assert success == True
        assert robot.get_position().x == 3
        assert robot.get_position().y == 2
        
        # Test up movement
        success = robot.move('up')
        assert success == True
        assert robot.get_position().x == 3
        assert robot.get_position().y == 3
        
        # Test left movement
        success = robot.move('left')
        assert success == True
        assert robot.get_position().x == 2
        assert robot.get_position().y == 3
        
        # Test down movement
        success = robot.move('down')
        assert success == True
        assert robot.get_position().x == 2
        assert robot.get_position().y == 2
        
        # Test backward movement (moves west/left)
        success = robot.move('backward')
        assert success == True
        assert robot.get_position().x == 1
        assert robot.get_position().y == 2
    
    def test_robot_boundary_detection(self):
        """Test robot boundary collision detection."""
        robot = Robot(0, 0)
        robot.set_grid_size(3, 3)
        
        # Test left boundary
        success = robot.move('left')
        assert success == False
        assert robot.get_position().x == 0  # Should not move
        assert robot.is_simulation_stopped() == True
        
        # Reset for next test
        robot.reset_simulation()
        
        # Test bottom boundary
        success = robot.move('down')
        assert success == False
        assert robot.get_position().y == 0  # Should not move
        assert robot.is_simulation_stopped() == True
        
        # Test top boundary
        robot.reset_simulation()
        robot.position.y = 2  # Move to top
        success = robot.move('up')
        assert success == False
        assert robot.get_position().y == 2  # Should not move
        
        # Test right boundary
        robot.reset_simulation()
        robot.position.x = 2  # Move to right edge
        success = robot.move('right')
        assert success == False
        assert robot.get_position().x == 2  # Should not move
    
    def test_wall_collision(self):
        """Test wall collision detection."""
        robot = Robot(1, 1)
        robot.set_grid_size(5, 5)
        robot.add_wall(2, 1)  # Add wall to the right
        robot.add_wall(1, 2)  # Add wall above
        
        # Test wall collision to the right
        success = robot.move('right')
        assert success == False
        assert robot.get_position().x == 1  # Should not move
        assert robot.is_simulation_stopped() == True
        
        # Reset and test wall collision upward
        robot.reset_simulation()
        success = robot.move('up')
        assert success == False
        assert robot.get_position().y == 1  # Should not move
    
    def test_invalid_direction(self):
        """Test handling of invalid movement directions."""
        robot = Robot(1, 1)
        robot.set_grid_size(5, 5)
        
        success = robot.move('invalid_direction')
        assert success == False
        assert robot.is_simulation_stopped() == True
    
    def test_robot_reset(self):
        """Test robot reset functionality."""
        robot = Robot(2, 2)
        robot.set_grid_size(5, 5)
        
        # Move robot and stop simulation
        robot.move('right')
        robot.move('left')  # This will hit boundary and stop
        robot.move('left')  # Should hit boundary
        
        initial_pos = robot.get_position()
        
        # Reset should restore to start position
        robot.reset_simulation()
        assert robot.get_position().x == 2
        assert robot.get_position().y == 2
        assert robot.is_simulation_stopped() == False
        assert len(robot.get_move_log()) == 0
    
    def test_move_logging(self):
        """Test move logging functionality."""
        robot = Robot(1, 1)
        robot.set_grid_size(5, 5)
        
        # Make some moves
        robot.move('right')
        robot.move('up')
        robot.add_wall(3, 2)  # Add wall
        robot.move('right')   # Should hit wall
        
        log = robot.get_move_log()
        assert len(log) == 3
        assert log[0]['direction'] == 'right'
        assert log[0]['success'] == True
        assert log[1]['direction'] == 'up'
        assert log[1]['success'] == True
        assert log[2]['direction'] == 'right'
        assert log[2]['success'] == False
        assert log[2]['reason'] == 'obstacle'


class TestPosition:
    """Test Position class functionality."""
    
    def test_position_creation(self):
        """Test position creation and properties."""
        pos = Position(3, 4)
        assert pos.x == 3
        assert pos.y == 4
    
    def test_position_equality(self):
        """Test position equality comparison."""
        pos1 = Position(2, 3)
        pos2 = Position(2, 3)
        pos3 = Position(2, 4)
        
        assert pos1 == pos2
        assert pos1 != pos3
    
    def test_position_string(self):
        """Test position string representation."""
        pos = Position(5, 7)
        assert str(pos) == "(5, 7)"


class TestRobotProgram:
    """Test the RobotProgram wrapper (without GUI)."""
    
    def test_program_creation(self):
        """Test robot program creation."""
        program = create_robot_program(8, 6, 2, 3)
        assert program.robot.get_position().x == 2
        assert program.robot.get_position().y == 3
        assert program.robot.grid_width == 8
        assert program.robot.grid_height == 6
    
    def test_add_wall_through_program(self):
        """Test adding walls through program interface."""
        program = create_robot_program(5, 5, 0, 0)
        program.add_wall(1, 0)
        
        # Try to move into wall
        success = program.robot.move('right')
        assert success == False
        assert program.robot.is_simulation_stopped() == True
    
    @patch('robot_behavior.simulator.enhanced_simulator.EnhancedSimulator')
    def test_program_has_simulator(self, mock_simulator):
        """Test that program creates simulator."""
        program = create_robot_program(5, 5, 0, 0)
        assert hasattr(program, 'simulator')


class TestDirections:
    """Test Direction enumeration."""
    
    def test_direction_values(self):
        """Test all direction enum values."""
        assert Direction.UP.value == "up"
        assert Direction.DOWN.value == "down"
        assert Direction.LEFT.value == "left"
        assert Direction.RIGHT.value == "right"
        assert Direction.BACKWARD.value == "backward"
    
    def test_direction_creation_from_string(self):
        """Test creating Direction from string values."""
        assert Direction("up") == Direction.UP
        assert Direction("down") == Direction.DOWN
        assert Direction("left") == Direction.LEFT
        assert Direction("right") == Direction.RIGHT
        assert Direction("backward") == Direction.BACKWARD


class TestMazeLayouts:
    """Test predefined maze layouts."""
    
    def test_simple_maze_structure(self):
        """Test that SIMPLE_MAZE has correct structure."""
        assert isinstance(SIMPLE_MAZE, list)
        assert len(SIMPLE_MAZE) > 0
        assert isinstance(SIMPLE_MAZE[0], list)
        
        # Check that maze contains expected characters
        maze_chars = set()
        for row in SIMPLE_MAZE:
            maze_chars.update(row)
        
        expected_chars = {'.', '#'}
        assert expected_chars.issubset(maze_chars)
    
    def test_student_maze_structure(self):
        """Test that STUDENT_MAZE has correct structure."""
        assert isinstance(STUDENT_MAZE, list)
        assert len(STUDENT_MAZE) > 0
        assert isinstance(STUDENT_MAZE[0], list)
        
        # Check for start position marker
        has_start = False
        for row in STUDENT_MAZE:
            if 'S' in row:
                has_start = True
                break
        
        assert has_start, "STUDENT_MAZE should contain start position 'S'"


class TestPackageIntegration:
    """Test package-level integration."""
    
    def test_package_imports(self):
        """Test that main package imports work correctly."""
        import robot_behavior
        
        # Test main function imports
        assert hasattr(robot_behavior, 'create_robot_program')
        assert hasattr(robot_behavior, 'Robot')
        assert hasattr(robot_behavior, 'Position')
        assert hasattr(robot_behavior, 'Direction')
        
        # Test version info
        assert hasattr(robot_behavior, '__version__')
        assert hasattr(robot_behavior, '__author__')
    
    def test_create_robot_program_integration(self):
        """Test full integration of create_robot_program."""
        from robot_behavior import create_robot_program
        
        program = create_robot_program(4, 4, 1, 1)
        
        # Test basic movement sequence
        moves = ['right', 'up', 'left', 'down']
        for move in moves:
            success = program.robot.move(move)
            assert success == True
            
        # Should be back at start position
        assert program.robot.get_position().x == 1
        assert program.robot.get_position().y == 1


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '--tb=short'])
