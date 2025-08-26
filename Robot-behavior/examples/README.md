# Robot Behavior Examples

This folder contains example code and templates for the unified student API.
All examples use the *same* calls (create_robot_program, run_with_visualization,
program.robot.move) and differ only by `mode="simulator"` vs `mode="real"`.

## 📁 Files Overview

### `minimal_api_examples.py`
Simulator-focused example demonstrating grid features:
- Creates a 5x5 grid with walls
- Shows the robot moving in a sequence
- Demonstrates all basic movement commands
- Perfect for teachers to show students what's possible

**Run this example:**
```bash
python examples/minimal_api_examples.py
```

### `student_template.py`
Starting template for students to write their own algorithms:
- Pre-configured setup code
- Clear comments explaining available commands
- TODO sections where students add their logic
- Example movements commented out for reference

**Students can copy and modify this file:**
```bash
cp examples/student_template.py my_robot_algorithm.py
# Edit my_robot_algorithm.py with your own code
python my_robot_algorithm.py
```

### `simulator_demo.py`
Concise demo using `mode="simulator"` plus a few sample walls.

### `real_robot_demo.py`
Real Unitree Go1 demo (no GUI) using the exact same movement API.
Before running ensure the robot is reachable and hardware dependencies are installed.

## 🎯 For Educators

Use the simulator demos to project and explain movement logic, then show
`real_robot_demo.py` to highlight that no new API is required for hardware.

## 🎓 For Students

1. Run `minimal_api_examples.py` or `simulator_demo.py` to see basic moves.
2. Copy `student_template.py` and build your own algorithm.
3. When ready for real hardware, switch only the `mode` parameter.

## 🚀 Student Assignment Ideas

- **Beginner**: Make the robot draw a square or triangle
- **Intermediate**: Navigate around obstacles to reach a goal
- **Advanced**: Implement maze-solving algorithms (BFS, A*, etc.)

Happy coding! 🤖
