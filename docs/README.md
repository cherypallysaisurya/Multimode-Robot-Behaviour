# 🤖 **UNIFIED ROBOT CONTROL SYSTEM**

A simple, clean interface that allows students to control both a 2D simulator and a real Go1 robot using identical code.

## 🚀 **Quick Start**

### **For Students:**
```python
from unified_robot import create_robot_program, run_with_visualization

program = create_robot_program()

def moves():
    program.robot.move("right")
    program.robot.move("up")
    program.robot.move("left")
    program.robot.move("down")

run_with_visualization(program, moves)
```

### **For Instructors:**
1. **Switch modes** in `unified_robot.py`:
   ```python
   MODE = "simulator"  # or "real"
   ```

2. **Set robot IP** for real robot:
   ```python
   ROBOT_SETTINGS = {
       "host": "YOUR_ROBOT_IP",  # Change this
   }
   ```

## 📁 **Project Structure**

```
Robot-behaviour-4/
├── 📄 unified_robot.py           # ⭐ MAIN SYSTEM - Core interface
├── 📄 student_simple_example.py  # ⭐ STUDENT TEMPLATE - Copy to start
├── 📄 README.md                  # This documentation
├── 📄 LICENSE                    # MIT License
├── 📄 pyproject.toml            # Python project config
├── 📄 PROJECT_STRUCTURE.md       # Detailed structure guide
│
├── 📁 examples/                  # 🎓 Student examples
│   └── (student example files)
│
├── 📁 docs/                      # 📚 Documentation
│   └── (system documentation)
│
├── 📁 Robot-behavior/            # 🎮 Simulator backend
│   └── (2D grid simulator implementation)
│
├── 📁 go1-py-main/               # 🤖 Real robot backend
│   └── (Go1 robot control library)
│
└── 📁 tests/                     # 🧪 Testing
    └── testing1.py              # Integration tests
```

## 🎯 **What Students Need**

### **Essential Files:**
- **`unified_robot.py`** - Import this in your code (don't edit)
- **`student_simple_example.py`** - Copy this as your starting template

### **Student Workflow:**
1. **Copy template**: `cp student_simple_example.py my_program.py`
2. **Edit moves**: Add your `program.robot.move()` commands
3. **Run**: `python my_program.py`

## ⚙️ **Configuration**

### **Switch Modes (Instructors):**
Edit `unified_robot.py`, line 1:
```python
MODE = "simulator"  # Visual 2D grid
MODE = "real"       # Actual robot control
```

### **Robot Settings:**
```python
ROBOT_SETTINGS = {
    "host": "192.168.1.100",    # Robot IP address
    "initial_mode": "Walk",     # Walking mode
    "move_speed": 0.3,          # Speed (0.1-1.0)
    "move_time": 1.0,           # Duration per move
}
```

## 🛡️ **Safety Features**

- ✅ **Automatic fallback**: Mock mode if robot unavailable
- ✅ **Error handling**: No crashes on connection failures
- ✅ **Same code**: Students' code works in both modes
- ✅ **Clean interface**: No complex imports needed

## 🎓 **Student Examples**

### **Basic Movement:**
```python
def moves():
    program.robot.move("right")
    program.robot.move("up")
```

### **Custom Grid:**
```python
program = create_robot_program(grid_width=10, grid_height=6)
```

### **With Obstacles:**
```python
program.add_wall(2, 3)
program.add_wall(4, 5)
```

## 🚀 **Ready for Presentation**

- ✅ **Students**: Simple `program.robot.move()` commands
- ✅ **Instructors**: Easy mode switching
- ✅ **Real robot**: Automatic connection and setup
- ✅ **Simulator**: Visual feedback and obstacles
- ✅ **Error-safe**: Never crashes, always works

---

**🎯 Get started: Copy `student_simple_example.py` and begin coding!**
