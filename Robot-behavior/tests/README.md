# Tests for robot-behavior-simulator

This directory contains tests for the robot-behavior-simulator package.

## Running Tests

To run the tests, install pytest and run:

```bash
pip install pytest
pytest tests/
```

Or run specific test files:

```bash
pytest tests/test_robot_behavior.py -v
```

## Test Coverage

The tests cover:
- Basic robot creation and movement
- Boundary detection
- Wall collision detection  
- Backward movement functionality
- RobotProgram wrapper functionality
- Direction enumeration

## Adding Tests

When adding new features, please add corresponding tests in this directory following the naming convention `test_*.py`.
