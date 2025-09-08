# 🤖 Unified Robot Control

A comprehensive educational robotics package that provides a **single, simple interface** for controlling both simulated and real robots. Perfect for computer science education where students learn with a visual simulator and seamlessly transition to real hardware.

## 🌟 Key Features

- **🎯 Unified API**: Same code works for both simulator and real Go1 robot
- **🎮 Visual Simulator**: Interactive 2D grid with robot trails and obstacles  
- **🤖 Real Robot Support**: Direct control of Unitree Go1 quadruped robot
- **📚 Educational Focus**: Designed for teaching programming fundamentals
- **🛡️ Robust Fallbacks**: Graceful handling when hardware isn't available
- **👨‍🎓 Student Friendly**: Simple `robot.move("direction")` interface

## 🚀 Quick Installation

```bash
# Install the complete package (works for both simulator and real robot)
pip install unified-robot-control
```

**That's it!** No additional setup needed. The package includes everything:
- ✅ Visual simulator with GUI
- ✅ Real robot communication libraries  
- ✅ Automatic fallbacks and error handling
- ✅ Student examples and templates

## 🎮 Quick Start - Simulator

```python
from unified_robot_control import create_robot_program

# Create a robot in a 6x6 grid world
program = create_robot_program(grid_width=6, grid_height=6)

# Add some obstacles
program.add_wall(3, 3)
program.add_wall(4, 3)

# Move the robot
program.robot.move("up")
program.robot.move("right") 
program.robot.move("down")
program.robot.move("left")

# Show the visual result
program.start()
```

## 🤖 Quick Start - Real Robot

```python
from unified_robot_control import create_robot_program

# Create real robot program (automatically detects hardware)
program = create_robot_program(mode="real")

# Same simple interface!
program.robot.move("up")     # Robot moves forward
program.robot.move("right")  # Robot turns right
program.robot.move("down")   # Robot moves backward  
program.robot.move("left")   # Robot turns left
```

## 🎓 For Students

### Basic Template
```python
from unified_robot_control import create_robot_program, run_with_visualization

def my_robot_program():
    # Create your robot world
    program = create_robot_program()
    
    # Add obstacles (simulator only)
    program.add_wall(2, 2)
    
    # Define your movements
    def moves():
        program.robot.move("right")
        program.robot.move("up")
        program.robot.move("left")
        program.robot.move("down")
    
    # Run with animation
    run_with_visualization(program, moves)

# Run your program
my_robot_program()
```

### Available Commands
```python
# Movement (works in both simulator and real robot)
program.robot.move("up")     # Forward/North
program.robot.move("down")   # Backward/South  
program.robot.move("left")   # Turn left/West
program.robot.move("right")  # Turn right/East

# Simulator-only features
program.add_wall(x, y)       # Add obstacle at position
program.start()              # Show visual simulation
```

## 👨‍🏫 For Instructors

### Easy Mode Switching

**Method 1: Environment Variable (Recommended for TAs)**
```bash
# Set once, affects all programs
export ROBOT_MODE=real        # Linux/Mac
set ROBOT_MODE=real          # Windows

python student_code.py       # Now uses real robot automatically
```

**Method 2: Code Parameter**
```python
# Simulator mode (default)
program = create_robot_program(mode="simulator")

# Real robot mode  
program = create_robot_program(mode="real")
```

**Method 3: Global Configuration**
```python
# In unified_robot_control/core.py
MODE = "real"  # Changes default for all programs
```

### Robot Configuration
```python
# Customize robot behavior (edit in core.py)
ROBOT_SETTINGS = {
    "host": "192.168.12.1",      # Robot IP address
    "initial_mode": "walk",      # Starting robot mode
    "move_speed": 0.3,           # Movement speed (0.0 to 1.0)
    "move_time": 1.0,            # Duration of each move in seconds
    "turn_speed": 0.3,           # Turning speed
    "turn_time": 1.0,            # Duration of each turn
}
```

## 🛠️ Advanced Usage

### Error Handling
```python
# Check if move was successful
success = program.robot.move("up")
if not success:
    print("Move blocked by obstacle or boundary")

# Robot hardware detection
from unified_robot_control.robot_hardware import is_real_robot_available
if is_real_robot_available("192.168.12.1"):
    print("Real robot is available")
else:
    print("Using simulator/mock mode")
```

### Custom Grid Sizes
```python
# Create custom simulator environments
program = create_robot_program(
    grid_width=12,
    grid_height=8, 
    start_x=4,
    start_y=3
)
```

### Visualization Control  
```python
# Run with custom timing
run_with_visualization(program, moves, move_delay=0.2)  # Faster
run_with_visualization(program, moves, move_delay=2.0)  # Slower
```

## 🔧 System Requirements

### For Simulator Mode
- **Python**: 3.10 or higher
- **GUI**: tkinter (included with Python)
- **Graphics**: Pillow (auto-installed)
- **Platform**: Windows, macOS, Linux

### For Real Robot Mode  
- **Network**: WiFi connection to Go1 robot
- **Robot**: Unitree Go1 quadruped robot
- **Libraries**: paho-mqtt, numpy (auto-installed)

### Installation Dependencies
```bash
# These are automatically installed:
pip install Pillow>=8.0.0      # Graphics support
pip install paho-mqtt>=2.0.0   # Robot communication  
pip install numpy>=1.20.0      # Math operations
```

## 🏗️ Package Architecture

```
unified-robot-control/
├── 🎮 simulator/           # Visual 2D simulator
├── 🤖 robot_hardware/      # Real robot interface  
├── 📦 go1_py/             # Go1 robot library (bundled)
├── 🎓 examples/           # Student templates
└── ⚙️ core.py            # Unified interface
```

### Key Design Principles
- **Single Interface**: Same API for simulator and real robot
- **Graceful Fallbacks**: Automatic mock mode when hardware unavailable
- **Educational Focus**: Simple commands, immediate feedback
- **Robust Error Handling**: Clear messages, no crashes
- **Easy Deployment**: One pip install, everything included

## 🎯 Educational Use Cases

### Computer Science Courses
- **CS1/Intro Programming**: Visual feedback for basic concepts
- **Algorithms**: Path planning, maze solving, pattern creation
- **Control Systems**: Real robot provides physical feedback
- **Software Engineering**: API design, error handling

### Classroom Activities
- **Maze Navigation**: Program robot to solve increasingly complex mazes
- **Pattern Drawing**: Create geometric shapes and artistic patterns
- **Obstacle Avoidance**: Navigate around dynamic environments  
- **Collaborative Coding**: Students work together on robot challenges

### Assessment Ideas
- **Code Review**: Students explain their robot movement algorithms
- **Debugging Exercises**: Fix broken robot programs
- **Creative Projects**: Design robot art or complex behaviors
- **Real Robot Demos**: Showcase working code on actual hardware

## 🔍 Troubleshooting

### Common Issues

**"Import Error: No module named 'unified_robot_control'"**
```bash
# Ensure package is installed
pip install unified-robot-control

# Check installation
pip list | grep unified-robot-control
```

**"Robot not moving in real mode"**
- Check robot IP address in `ROBOT_SETTINGS`
- Ensure robot is on same WiFi network
- Verify robot is powered on and ready
- System automatically falls back to mock mode if robot unreachable

**"Simulator window not appearing"**
- Ensure tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt install python3-tk`
- Check for GUI environment (some servers don't support graphics)

**"Permission denied on robot commands"**
- Check robot WiFi connection
- Verify robot IP address
- Ensure robot is in correct mode (not in safety lockout)

### Getting Help
- 📖 **Documentation**: Check docstrings with `help(create_robot_program)`
- 🐛 **Issues**: Report bugs at [GitHub Issues](https://github.com/cherypallysaisurya/Multimode-Robot-Behaviour/issues)
- 💬 **Discussions**: Ask questions at [GitHub Discussions](https://github.com/cherypallysaisurya/Multimode-Robot-Behaviour/discussions)

## 🤝 Contributing

We welcome contributions from educators and developers!

### Development Setup
```bash
# Clone repository
git clone https://github.com/cherypallysaisurya/Multimode-Robot-Behaviour.git
cd Multimode-Robot-Behaviour

# Install in development mode
pip install -e .

# Run tests
python test_package.py
```

### Areas for Contribution
- 📚 Educational examples and tutorials
- 🐛 Bug fixes and improvements  
- 🌍 Internationalization (i18n)
- 🤖 Support for additional robot models
- 📖 Documentation improvements

## 📄 License & Credits

### License
MIT License - Free for educational and commercial use!

### Credits
- **Lead Developer**: Sai Surya Cherrypally
- **Educational Consultants**: Computer science educators worldwide
- **Robot Integration**: Unitree Go1 community
- **Simulator Graphics**: Built with Python Tkinter and Pillow

### Acknowledgments
Special thanks to:
- 🐍 Python community for excellent libraries
- 🎓 Educators providing feedback and requirements
- 🤖 Robotics community for technical guidance
- 👥 Open source contributors worldwide

---

## 🚀 Ready to Start?

```bash
# Install the package
pip install unified-robot-control

# Create your first robot program
echo "
from unified_robot_control import create_robot_program

program = create_robot_program()
program.robot.move('right')
program.robot.move('up')
program.start()
" > my_robot.py

# Run it!
python my_robot.py
```

**🎉 Welcome to the world of educational robotics!**

---

<div align="center">

**⭐ Star this repo if you find it helpful for education!**

**🔔 Watch for updates and new educational features!**

**📢 Share with other educators and students!**

</div>
