import random
from time import sleep

import numpy as np
import paho.mqtt.client as mqtt

from go1_py.parsers import bms_parser, robot_parser
from go1_py.state import BMS, Robot


class Dog:
    def __init__(self, host = "192.168.12.1"):
        self.robot = Robot()
        self.bms = BMS()

        client = mqtt.Client(
            client_id=f"go1-py-{random.randint(0, 1000)}",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        client.on_message = self.on_message
        client.connect(host, 1883, keepalive=5)
        client.loop_start()
        client.subscribe("firmware/version")
        client.subscribe("bms/state")
        self.client = client

        while not self.client.is_connected():
            sleep(0.1)

    def on_message(self, client, userdata, msg):
        payload = np.frombuffer(msg.payload, dtype=np.uint8)
        match msg.topic:
            case "firmware/version":
                self.robot = robot_parser(payload)
            case "bms/state":
                self.bms = bms_parser(payload)

    def change_mode(self, mode):
        self.stop_moving()
        self.client.publish("controller/action", mode.value, qos=1)

    def change_led_color(self, r, g, b):
        self.client.publish(
            "programming/code", f"child_conn.send('change_light({r},{g},{b})')", qos=0
        )

    def move(self, x, y, z, w):
        self.client.publish(
            "controller/stick",
            np.array([x, y, z, w], dtype=np.float32).clip(-1, 1).tobytes(),
            qos=0,
        )

    def stop_moving(self):
        self.move(0, 0, 0, 0)

    def move_over_time(self, x, y, z, w, t):
        FREQ = 10
        for _ in range(int(FREQ * t)):
            self.move(x, y, z, w)
            sleep(1 / FREQ)
        self.stop_moving()

    def go_forward(self, speed, time):
        self.move_over_time(0, 0, 0, speed, time)

    def go_backward(self, speed, time):
        self.go_forward(-speed, time)

    def go_right(self, speed, time):
        self.move_over_time(speed, 0, 0, 0, time)

    def go_left(self, speed, time):
        self.go_right(-speed, time)

    def turn_right(self, speed, time):
        self.move_over_time(0, speed, 0, 0, time)

    def turn_left(self, speed, time):
        self.turn_right(-speed, time)

    def extend_up(self, speed, time):
        self.move_over_time(0, 0, 0, speed, time)

    def squat_down(self, speed, time):
        self.extend_up(-speed, time)

    def lean_right(self, speed, time):
        self.move_over_time(speed, 0, 0, 0, time)

    def lean_left(self, speed, time):
        self.lean_right(-speed, time)

    def twist_right(self, speed, time):
        self.move_over_time(0, speed, 0, 0, time)

    def twist_left(self, speed, time):
        self.twist_right(-speed, time)

    def look_down(self, speed, time):
        self.move_over_time(0, 0, speed, 0, time)

    def look_up(self, speed, time):
        self.look_down(-speed, time)


