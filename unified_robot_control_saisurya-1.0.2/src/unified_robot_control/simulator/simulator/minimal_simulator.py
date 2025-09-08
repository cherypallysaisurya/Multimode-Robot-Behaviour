import tkinter as tk
from tkinter import messagebox
from typing import Set, Tuple, Optional
from ..core.robot import Robot, Position
import os
from PIL import Image, ImageTk
import time

class MinimalSimulator:
    """
    Educational simulator with smooth movement.
    
    Features:
    - 10x10 grid with solid arrow robot pointing east
    - Smooth animated movement between cells
    - Auto-retry on wall collision with popup message
    - Proper timing for educational visualization
    """
    
    def __init__(self, robot: Robot, cell_size: int = 50):
        self.robot = robot
        self.cell_size = cell_size
        self.running = False
        self.root = None
        self.canvas = None
        self.robot_image = None
        self.robot_item = None
        self.movement_trail = []  # Store path for red line
        self.wall_hit = False
        
        # Create robot arrow
        self._create_robot_arrow()
    
    def _create_robot_arrow(self):
        """Create a solid arrow pointing east for the robot."""
        self.robot_image = None  # Will be created after tkinter root is available
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🤖 Robot Simulator")
        self.root.configure(bg="white")
        
        # Create title label
        self.title_label = tk.Label(
            self.root,
            text="Educational Robot Simulator",
            font=("Arial", 14, "bold"),
            fg="#1f2937",
            bg="white",
            pady=10
        )
        self.title_label.pack()
        
        # Create info frame
        self.info_frame = tk.Frame(self.root, bg="white")
        self.info_frame.pack(pady=5)
        
        self.position_label = tk.Label(
            self.info_frame,
            text=f"Position: {self.robot.get_position()}",
            font=("Arial", 10),
            fg="#374151",
            bg="white"
        )
        self.position_label.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(
            self.info_frame,
            text="Ready",
            font=("Arial", 10),
            fg="#059669",
            bg="white"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Create canvas
        canvas_width = self.robot.grid_width * self.cell_size
        canvas_height = self.robot.grid_height * self.cell_size
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            highlightthickness=2,
            highlightbackground="#d1d5db"
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Create control frame
        self.control_frame = tk.Frame(self.root, bg="white")
        self.control_frame.pack(pady=5)
        
        # Reset button
        self.reset_button = tk.Button(
            self.control_frame,
            text="🔄 Reset Robot",
            command=self.reset_robot,
            font=("Arial", 10),
            bg="#f3f4f6",
            fg="#374151",
            relief="solid",
            borderwidth=1
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Close button
        self.close_button = tk.Button(
            self.control_frame,
            text="❌ Close",
            command=self.close,
            font=("Arial", 10),
            bg="#fee2e2",
            fg="#dc2626",
            relief="solid",
            borderwidth=1
        )
        self.close_button.pack(side=tk.LEFT, padx=5)
        
        # Draw initial state
        self.update_display()
    
    def update_display(self):
        """Update the visual display of the grid, robot, and obstacles."""
        self.canvas.delete("all")
        
        # Draw grid
        self._draw_grid()
        
        # Draw walls
        self._draw_walls()
        
        # Draw robot
        self._draw_robot()
        
        # Update info labels
        self.position_label.config(text=f"Position: {self.robot.get_position()}")
        
        if self.robot.is_simulation_stopped():
            self.status_label.config(text="❌ Stopped (Hit obstacle)", fg="#dc2626")
        else:
            self.status_label.config(text="✅ Running", fg="#059669")
        
        self.root.update()
    
    def _draw_grid(self):
        """Draw clean grid lines."""
        # Vertical lines
        for i in range(self.robot.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.robot.grid_height * self.cell_size,
                fill="#d1d5db", width=1
            )
        
        # Horizontal lines
        for i in range(self.robot.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(
                0, y, self.robot.grid_width * self.cell_size, y,
                fill="#d1d5db", width=1
            )
    
    def _draw_walls(self):
        """Draw walls/obstacles."""
        for x, y in self.robot.walls:
            # Convert to canvas coordinates (y=0 at top for tkinter)
            canvas_x = x * self.cell_size
            canvas_y = (self.robot.grid_height - 1 - y) * self.cell_size
            
            self.canvas.create_rectangle(
                canvas_x + 1, canvas_y + 1,
                canvas_x + self.cell_size - 1,
                canvas_y + self.cell_size - 1,
                fill="#374151", outline="#1f2937", width=2
            )
    
    def _draw_robot(self):
        """Draw the robot at its current position."""
        pos = self.robot.get_position()
        
        # Convert to canvas coordinates
        canvas_x = pos.x * self.cell_size
        canvas_y = (self.robot.grid_height - 1 - pos.y) * self.cell_size
        
        # Draw robot as a circle
        padding = 8
        self.canvas.create_oval(
            canvas_x + padding, canvas_y + padding,
            canvas_x + self.cell_size - padding,
            canvas_y + self.cell_size - padding,
            fill="#3b82f6", outline="#1d4ed8", width=2
        )
        
        # Draw robot direction indicator (small arrow)
        center_x = canvas_x + self.cell_size // 2
        center_y = canvas_y + self.cell_size // 2
        
        self.canvas.create_text(
            center_x, center_y,
            text="🤖", font=("Arial", int(self.cell_size * 0.4))
        )
    
    def reset_robot(self):
        """Reset robot to starting position."""
        self.robot.reset_simulation()
        self.update_display()
        print("🔄 Simulator: Robot reset to starting position")
    
    def set_title(self, title: str):
        """Set the simulator window title."""
        self.title_label.config(text=title)
    
    def start(self):
        """Start the simulator and keep it running."""
        self.running = True
        print("🖥️  Simulator window opened - close window or press Ctrl+C to exit")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⏹️ Simulator closed by user")
            self.close()
    
    def start_with_delay(self, delay_seconds: int = 5):
        """Start simulator and automatically close after delay."""
        self.running = True
        print(f"🖥️  Simulator will stay open for {delay_seconds} seconds...")
        
        def auto_close():
            print(f"⏰ Auto-closing simulator after {delay_seconds} seconds")
            self.close()
        
        # Schedule auto-close
        self.root.after(delay_seconds * 1000, auto_close)
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⏹️ Simulator closed by user")
            self.close()
    
    def close(self):
        """Close the simulator."""
        self.running = False
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass  # Handle case where window is already closed

class RobotProgram:
    """
    Minimal wrapper for educational robot programming.
    
    Provides the basic setup needed for student exercises:
    - Robot instance with movement API
    - Visual simulator 
    - Maze loading capability
    """
    
    def __init__(self, width: int = 10, height: int = 10, start_x: int = 0, start_y: int = 0):
        # Create robot
        self.robot = Robot(start_x, start_y)
        self.robot.grid_width = width
        self.robot.grid_height = height

        # Prevent starting inside a wall (in case user pre-populates walls externally)
        if (start_x, start_y) in getattr(self.robot, 'walls', set()):
            raise ValueError(f"Robot cannot start inside a wall at ({start_x}, {start_y})")
        
        # Create simulator
        self.simulator = MinimalSimulator(self.robot)
        
        print(f"🤖 Robot Program initialized: {width}x{height} grid")
        print(f"📍 Robot starting position: ({start_x}, {start_y})")
        print("📖 Available commands: robot.move('up'/'down'/'left'/'right')")
        print("🔧 Use robot.get_position() to check current location")
        print("⚠️  Simulation stops on illegal moves - use robot.reset_simulation() to continue")
    
    def add_wall(self, x: int, y: int):
        """Add a wall at the specified position."""
        self.robot.add_wall(x, y)
        if hasattr(self, 'simulator'):
            self.simulator.update_display()
    
    def load_maze(self, layout):
        """Load a maze layout."""
        self.robot.load_maze(layout)
        if hasattr(self, 'simulator'):
            self.simulator.update_display()
    
    def start(self):
        """Start the visual simulator."""
        print("🚀 Starting simulator...")
        self.simulator.start()
    
    def start_with_auto_close(self, delay_seconds: int = 5):
        """Start simulator and auto-close after specified seconds."""
        print(f"🚀 Starting simulator (will auto-close in {delay_seconds}s)...")
        self.simulator.start_with_delay(delay_seconds)
    
    def update_display(self):
        """Update the visual display after robot moves."""
        if hasattr(self, 'simulator'):
            self.simulator.update_display()
    
    def move_with_delay(self, direction: str, delay_seconds: float = 0.5):
        """Move robot with visual delay for better viewing."""
        import time
        success = self.robot.move(direction)
        self.update_display()
        time.sleep(delay_seconds)
        return success
