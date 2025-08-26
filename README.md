# myrobot

Unified educational robot API: 2D grid simulator + optional real Go1 robot control through `go1_py`.

## Install

Basic (simulator only):
```
pip install myrobot
```
Simulator + hardware extras:
```
pip install myrobot[hardware]
```
Add visual image dependencies (placeholder currently):
```
pip install myrobot[visual]
```

## Quick Start
```python
from myrobot import create_robot_program, run_with_visualization

program = create_robot_program(mode="simulator")

def moves():
    program.robot.move("up")
    program.robot.move("right")

run_with_visualization(program, moves)
```

Real robot (auto Walk mode):
```python
from myrobot import create_robot_program
program = create_robot_program(mode="real", host="go1-max")
program.robot.move("up", speed=0.4, time=1.5)
```

Mock real mode (no hardware needed):
```bash
set ROBOT_BEHAVIOR_HARDWARE_MOCK=1  # Windows PowerShell: $env:ROBOT_BEHAVIOR_HARDWARE_MOCK=1
```
```python
program = create_robot_program(mode="real")  # uses mock
```

## Environment Variable
- `ROBOT_BEHAVIOR_HARDWARE_MOCK=1` forces mock Dog (no MQTT)

## Testing
```bash
pytest -q
```

## Publishing (summary)
See CONTRIBUTING.md.
