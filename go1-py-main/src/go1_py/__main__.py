from objprint import op
from go1_py import Dog, Mode
from sshkeyboard import listen_keyboard_manual
import asyncio

dog = Dog()
dog.change_mode(Mode.Walk)

keys = {
    'w': 0,
    'a': 0,
    's': 0,
    'd': 0,
    'q': 0,
    'e': 0
}

def press(key):
    keys[key] = 1

def release(key):
    keys[key] = 0

async def loop():
    MOVE_SPEED = 0.3
    TURN_SPEED = 0.6
    while True:
        dog.move(MOVE_SPEED * (keys['d'] - keys['a']), TURN_SPEED * (keys['e'] - keys['q']), 0, MOVE_SPEED * (keys['w'] - keys['s']))
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(
        listen_keyboard_manual(
            press,
            release,
        ),
        loop()
    )

asyncio.run(main())
