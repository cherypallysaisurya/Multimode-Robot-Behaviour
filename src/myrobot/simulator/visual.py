"""Full enhanced simulator (Tkinter) ported from legacy project."""
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from typing import Optional
from ..core.robot import Position
from PIL import Image, ImageTk, ImageDraw  # type: ignore
import time

class EnhancedSimulator:
    def __init__(self, robot, cell_size: int = 60):
        self.robot = robot
        self.cell_size = cell_size
        self.running = False
        self.root = None
        self.canvas = None
        self.robot_image = None
        self.robot_item = None
        self.movement_trail = []
        self.trail_lines = []
        self.animating = False
        self._move_queue = []

    def _create_robot_circle(self):  # simpler icon
        try:
            diameter = int(self.cell_size * 0.58)
            img = Image.new('RGBA', (diameter, diameter), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            padding = max(2, diameter // 14)
            bbox = [padding, padding, diameter - padding, diameter - padding]
            draw.ellipse(bbox, fill=(59,130,246,255), outline=(17,94,198,255), width=max(2, diameter // 22))
            self.robot_image = ImageTk.PhotoImage(img)
        except Exception:
            self.robot_image = None

    def _setup(self):
        self.root = tk.Tk()
        self.root.title('Educational Robot Simulator')
        self._create_robot_circle()
        self.canvas = tk.Canvas(self.root, width=self.robot.grid_width * self.cell_size,
                                height=self.robot.grid_height * self.cell_size, bg='white')
        self.canvas.pack()
        self.movement_trail = [self.robot.get_position()]
        self._draw_scene()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _draw_scene(self):
        self.canvas.delete('all')
        for i in range(self.robot.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.robot.grid_height * self.cell_size, fill="#eee")
        for i in range(self.robot.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.robot.grid_width * self.cell_size, y, fill="#eee")
        for x, y in self.robot.walls:
            cx = x * self.cell_size
            cy = (self.robot.grid_height - 1 - y) * self.cell_size
            self.canvas.create_rectangle(cx+2, cy+2, cx+self.cell_size-2, cy+self.cell_size-2, fill='#333')
        self._draw_robot()

    def _draw_robot(self):
        pos = self.robot.get_position()
        cx = pos.x * self.cell_size + self.cell_size // 2
        cy = (self.robot.grid_height - 1 - pos.y) * self.cell_size + self.cell_size // 2
        if self.robot_image:
            self.robot_item = self.canvas.create_image(cx, cy, image=self.robot_image)
        else:
            self.robot_item = self.canvas.create_text(cx, cy, text='⚪', font=('Arial', int(self.cell_size*0.8)))

    def start_visualization(self, auto_close_seconds: Optional[int] = None):
        if self.running: return
        self.running = True
        self._setup()
        try:
            self.root.mainloop()
        except tk.TclError:
            pass
        finally:
            self.running = False

    def animate_move_with_trail(self, old_pos: Position, new_pos: Position, move_delay: float = 1.5):
        if not self.robot_item or self.animating: return
        self.animating = True
        old_x = old_pos.x * self.cell_size + self.cell_size // 2
        old_y = (self.robot.grid_height - 1 - old_pos.y) * self.cell_size + self.cell_size // 2
        new_x = new_pos.x * self.cell_size + self.cell_size // 2
        new_y = (self.robot.grid_height - 1 - new_pos.y) * self.cell_size + self.cell_size // 2
        steps = 30
        total_ms = int(move_delay * 1000)
        delay = max(1, total_ms // steps)
        dx = (new_x - old_x) / steps
        dy = (new_y - old_y) / steps
        def step(i: int):
            if not self.robot_item: return
            if i <= steps:
                self.canvas.coords(self.robot_item, old_x + dx*i, old_y + dy*i)
                if i < steps:
                    self.root.after(delay, lambda: step(i+1))
                else:
                    self._draw_trail_segment(old_pos, new_pos)
                    self.animating = False
                    if self._move_queue:
                        nxt_old, nxt_new, nxt_delay = self._move_queue.pop(0)
                        self.animate_move_with_trail(nxt_old, nxt_new, nxt_delay)
        step(0)

    def robot_moved(self, old_pos: Position, new_pos: Position, success: bool, move_delay: float = 1.5):
        if not self.canvas: return
        if success:
            old_copy = Position(old_pos.x, old_pos.y)
            new_copy = Position(new_pos.x, new_pos.y)
            self.movement_trail.append(new_copy)
            if self.animating:
                self._move_queue.append((old_copy, new_copy, move_delay))
            else:
                self.animate_move_with_trail(old_copy, new_copy, move_delay)
        else:
            messagebox.showwarning('Wall Hit', 'Robot hit a wall; resetting.')
            self._reset_robot()

    def _draw_trail_segment(self, start_pos: Position, end_pos: Position):
        if start_pos.x == end_pos.x and start_pos.y == end_pos.y: return
        sx = start_pos.x * self.cell_size + self.cell_size // 2
        sy = (self.robot.grid_height - 1 - start_pos.y) * self.cell_size + self.cell_size // 2
        ex = end_pos.x * self.cell_size + self.cell_size // 2
        ey = (self.robot.grid_height - 1 - end_pos.y) * self.cell_size + self.cell_size // 2
        line = self.canvas.create_line(sx, sy, ex, ey, fill='#ff0000', width=6, capstyle=tk.ROUND, tags='trail')
        self.canvas.tag_lower(line)

    def _reset_robot(self):
        self.robot.reset_simulation()
        self.movement_trail.append(self.robot.get_position())
        self._draw_scene()

    def _close(self):
        self.running = False
        try:
            if self.root:
                self.root.quit(); self.root.destroy()
        except Exception:
            pass

__all__ = ['EnhancedSimulator']
