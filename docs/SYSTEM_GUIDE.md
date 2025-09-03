# 📚 System Documentation

## 🏗️ **System Architecture**

The Unified Robot Control System is a wrapper that unifies two different APIs:

### **Backend APIs:**
1. **Robot-behavior** (Simulator): 2D grid-based visual simulator
2. **go1_py** (Real Robot): Go1 quadruped robot control library

### **Unified Interface:**
- **unified_robot.py**: Single interface that wraps both APIs
- **Students**: Only see `program.robot.move("direction")`
- **Instructors**: Control backend via simple configuration

## ⚙️ **Configuration Guide**

### **Mode Switching:**
```python
# In unified_robot.py, line 1:
MODE = "simulator"  # Visual 2D grid with GUI
MODE = "real"       # Controls actual robot
```

### **Robot Settings:**
```python
ROBOT_SETTINGS = {
    "host": "192.168.1.100",     # Robot IP address
    "initial_mode": "Walk",      # Robot walking mode
    "move_speed": 0.3,           # Movement speed (0.1 to 1.0)
    "move_time": 1.0,            # Duration of each move
    "turn_speed": 0.3,           # Turning speed (0.1 to 1.0)
    "turn_time": 1.0,            # Duration of each turn
}
```

### **Simulator Settings:**
```python
SIMULATOR_SETTINGS = {
    "grid_width": 8,             # Grid width
    "grid_height": 8,            # Grid height
    "start_x": 0,                # Starting X position
    "start_y": 0,                # Starting Y position
    "visualization_delay": 0.5,  # Delay between moves
}
```

## 🔄 **API Translation**

### **Student Code:**
```python
program.robot.move("up")     # Student's simple command
```

### **Simulator Backend:**
```python
self._backend.robot.move("up")  # Calls simulator API
```

### **Real Robot Backend:**
```python
self._dog.go_forward(0.3, 1.0)  # Calls go1_py API
```

## 🛡️ **Error Handling**

### **Connection Failures:**
- Real robot not available → Automatic mock mode
- Simulator not available → Error message with fallback

### **Mock Mode:**
- Prints movement commands to console
- Same interface as real robot
- Perfect for development and testing

## 🎯 **Customization Points**

### **Movement Mapping:**
Edit `_move_real_robot()` method to change how directions map to robot commands.

### **Speed Control:**
Modify `_get_movement_params()` to adjust speed/time based on direction.

### **Error Behavior:**
Update exception handling in `_setup_real_robot()` for custom fallbacks.

## 📋 **Maintenance**

### **Adding New Movements:**
1. Add to `_move_real_robot()` method
2. Add corresponding simulator support
3. Update student documentation

### **Backend Updates:**
- **Robot-behavior**: Update in Robot-behavior/ directory
- **go1_py**: Update in go1-py-main/ directory
- **Unified interface**: No changes needed (automatic)

## 🚀 **Deployment**

### **For Development:**
- Use simulator mode for testing
- Mock mode works without any robot hardware

### **For Real Robot:**
1. Ensure robot is on same WiFi network
2. Update ROBOT_SETTINGS["host"] with actual IP
3. Change MODE to "real"
4. System handles everything else automatically

The system is designed to be robust, educational, and presentation-ready!
