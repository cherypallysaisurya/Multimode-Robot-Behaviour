from nicegui import ui, app
from nicegui.events import KeyEventArguments
from go1_py import Dog, Mode
import asyncio
import requests

dog = Dog("go1-max")
dog.change_mode(Mode.Walk)

keys = {
    'KeyW': 0,
    'KeyA': 0,
    'KeyS': 0,
    'KeyD': 0,
    'KeyQ': 0,
    'KeyE': 0,
    'ShiftLeft': 0
}

def handle_key(e: KeyEventArguments):
    if e.key.code in keys.keys() and not e.action.repeat:
        value = 1 if e.action.keydown else 0
        keys[e.key.code] = value

async def loop():
    while True:
        if modes.value == "Stand":
            dog.move(keys['KeyE'] - keys['KeyQ'], 0.4 * (keys['KeyD'] - keys['KeyA']), -(keys['KeyW'] - keys['KeyS']), 0)
        else:
            MOVE_SPEED = 0.3 * (1 + 2 * keys['ShiftLeft'])
            TURN_SPEED = 0.6 * (1 + 2 * keys['ShiftLeft'])
            dog.move(MOVE_SPEED * (keys['KeyD'] - keys['KeyA']), TURN_SPEED * (keys['KeyE'] - keys['KeyQ']), 0, MOVE_SPEED * (keys['KeyW'] - keys['KeyS']))
        battery.set_text(f"{dog.bms.soc}%")
        await asyncio.sleep(0.1)

def change_mode(value):
    value = value.value
    match value:
        case "Damping":
            value = Mode.Damping
        case "StandDown":
            value = Mode.StandDown
        case "StandUp":
            value = Mode.StandUp
        case "Stand":
            value = Mode.Stand
        case "Walk":
            value = Mode.Walk
        case "Run":
            value = Mode.Run
        case "Climb":
            value = Mode.Climb
    dog.change_mode(value)

app.on_startup(loop)

ui.add_css("""
""")
ui.keyboard(on_key=handle_key)
modes = ui.toggle(["Damping", "StandDown", "StandUp", "Stand", "Walk", "Run", "Climb"], value="Walk", on_change = change_mode)
battery = ui.label("")
ui.image("http://go1-max:5000/front").style("height: 400px; width: 400px;")
ui.add_body_html("<iframe src='http://go1-max:8889/sound/'></iframe>")

with ui.button_group():
    ui.button("Bark", on_click=lambda: requests.get("http://go1-max:5000/sound/dog"))
    ui.button("Neigh", on_click=lambda: requests.get("http://go1-max:5000/sound/horse"))

ui.run()
