import tkinter as tk
from tkinter import messagebox
from typing import Set, Tuple, Optional, List
from ..core.robot import Robot, Position
import os
from PIL import Image, ImageTk, ImageDraw
import time
import threading

class EnhancedSimulator:
    """
    Enhanced educational simulator with all requested features:
    - 10x10 grid with dog.png robot image
    - Red line trail showing robot movement path
    - Smooth animated movement between cells
    - Auto-retry on wall collision with popup message
    - Proper timing for educational visualization
    """
    def __init__(self, robot: Robot, cell_size: int = 60):
        """Initialize simulator state and defer heavy GUI creation until start."""
        # Core references
        self.robot = robot
        self.cell_size = cell_size

        # GUI state placeholders (created later)
        self.running = False
        self.root = None
        self.canvas = None

        # Visual elements (created after Tk root exists)
        self.robot_image = None
        self.robot_item = None

        # Movement & trail tracking
        self.movement_trail = []  # list of Position objects representing path
        self.trail_lines = []     # list of canvas line ids
        self.animating = False
        self._move_queue = []     # queued moves: (old_pos, new_pos, delay)

        # (robot_image stays None until _create_robot_arrow runs)
    
    def _create_robot_arrow(self):
        """Create a simple solid circular robot icon with outline."""
        try:
            # Circle diameter reduced for better spacing inside the cell
            diameter = int(self.cell_size * 0.58)
            img = Image.new('RGBA', (diameter, diameter), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            padding = max(2, diameter // 14)
            bbox = [padding, padding, diameter - padding, diameter - padding]

            fill_color = (59, 130, 246, 255)      # Primary blue
            outline_color = (17, 94, 198, 255)    # Darker outline
            draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=max(2, diameter // 22))

            self.robot_image = ImageTk.PhotoImage(img)
            print("🔵 Created solid circular robot icon")
        except Exception as e:
            print(f"⚠️ Error creating solid circle: {e}, falling back to text")
            self.robot_image = None
    
    def _setup_window(self):
        """Setup the main window and UI components with improved styling."""
        # Create main window
        self.root = tk.Tk()
        self.root.title("🤖 Robot Simulator")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        
        # Now that root window exists, create robot arrow
        self._create_robot_arrow()
        
        # Create title frame with better spacing
        title_frame = tk.Frame(self.root, bg="white", height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        # Enhanced title with professional styling
        title_label = tk.Label(
            title_frame,
            text="🤖 Educational Robot Simulator",
            font=("Arial", 16, "bold"),
            fg="#2563eb",  # Professional blue
            bg="white",
            pady=15
        )
        title_label.pack()
        
        # Info frame with better styling
        info_frame = tk.Frame(self.root, bg="white")
        info_frame.pack(pady=5)
        
        self.position_label = tk.Label(
            info_frame,
            text=f"Position: {self.robot.get_position()}",
            font=("Arial", 12),
            fg="#374151",
            bg="white"
        )
        self.position_label.pack(side=tk.LEFT, padx=15)
        
        self.status_label = tk.Label(
            info_frame,
            text="Ready to move",
            font=("Arial", 12),
            fg="#059669",
            bg="white"
        )
        self.status_label.pack(side=tk.LEFT, padx=15)
        
        # Create canvas with professional styling
        canvas_width = self.robot.grid_width * self.cell_size
        canvas_height = self.robot.grid_height * self.cell_size
        
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            highlightthickness=2,
            highlightbackground="#e5e7eb",  # Professional light gray border
            relief="solid"
        )
        self.canvas.pack(padx=15, pady=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="white")
        control_frame.pack(pady=10)
        
        reset_button = tk.Button(
            control_frame,
            text="🔄 Reset & Retry",
            command=self._reset_robot,
            font=("Arial", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            padx=20,
            pady=5
        )
        reset_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(
            control_frame,
            text="❌ Close",
            command=self._close,
            font=("Arial", 12),
            bg="#ef4444",
            fg="white",
            relief="flat",
            padx=20,
            pady=5
        )
        close_button.pack(side=tk.LEFT, padx=10)
        
        # Initialize trail with starting position
        start_pos = self.robot.get_position()
        self.movement_trail = [start_pos]
        
        # Draw initial state
        self._draw_complete_scene()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._close)
    
    def _draw_complete_scene(self):
        """Draw the complete scene: grid, walls, trail, and robot."""
        # Clear everything except trail lines
        items_to_delete = self.canvas.find_all()
        for item in items_to_delete:
            tags = self.canvas.gettags(item)
            if "trail" not in tags:
                self.canvas.delete(item)
        
        # Draw grid
        self._draw_grid()
        
        # Draw walls
        self._draw_walls()
        
        # Draw movement trail (for any segments not yet drawn)
        self._draw_movement_trail()
        
        # Draw robot
        self._draw_robot()
        
        # Update status
        self._update_status()
    
    def _draw_grid(self):
        """Draw clean grid lines for the specified grid size."""
        # Vertical lines
        for i in range(self.robot.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.robot.grid_height * self.cell_size,
                fill="#e5e7eb", width=1
            )
        
        # Horizontal lines
        for i in range(self.robot.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(
                0, y, self.robot.grid_width * self.cell_size, y,
                fill="#e5e7eb", width=1
            )
    
    def _draw_walls(self):
        """Draw walls/obstacles."""
        for x, y in self.robot.walls:
            # Convert to canvas coordinates (y=0 at top for tkinter)
            canvas_x = x * self.cell_size
            canvas_y = (self.robot.grid_height - 1 - y) * self.cell_size
            
            self.canvas.create_rectangle(
                canvas_x + 2, canvas_y + 2,
                canvas_x + self.cell_size - 2,
                canvas_y + self.cell_size - 2,
                fill="#374151", outline="#1f2937", width=2
            )
            
            # Add wall symbol
            center_x = canvas_x + self.cell_size // 2
            center_y = canvas_y + self.cell_size // 2
            self.canvas.create_text(
                center_x, center_y,
                text="🧱", font=("Arial", int(self.cell_size * 0.4))
            )
    
    def _draw_movement_trail(self):
        """Draw red line trail showing robot's path (for initial setup only)."""
        # Skip drawing trail during real-time movement - trails are drawn individually
        return
    
    def _draw_robot(self):
        """Draw the robot (solid arrow pointing east) at current position."""
        pos = self.robot.get_position()
        
        # Convert to canvas coordinates
        canvas_x = pos.x * self.cell_size
        canvas_y = (self.robot.grid_height - 1 - pos.y) * self.cell_size
        
        # Calculate center position
        center_x = canvas_x + self.cell_size // 2
        center_y = canvas_y + self.cell_size // 2
        
        if self.robot_image:
            # Use circular image
            self.robot_item = self.canvas.create_image(
                center_x, center_y,
                image=self.robot_image
            )
        else:
            # Use simple text triangle as fallback
            self.robot_item = self.canvas.create_text(center_x, center_y, text="⚪", font=("Arial", int(self.cell_size * 0.8)), fill="#0064c8")
    
    def _update_status(self):
        """Update position and status labels."""
        if hasattr(self, 'position_label'):
            self.position_label.config(text=f"Position: {self.robot.get_position()}")
        
        if hasattr(self, 'status_label'):
            if self.robot.is_simulation_stopped():
                self.status_label.config(text="❌ Stopped - Hit Wall!", fg="#dc2626")
            else:
                self.status_label.config(text="✅ Moving", fg="#059669")
    
    def animate_move_with_trail(self, old_pos: Position, new_pos: Position, move_delay: float = 1.5):
        """Animate movement and draw trail when animation completes."""
        if not self.robot_item or self.animating:
            return
        
        self.animating = True
        
        # Calculate canvas coordinates
        old_x = old_pos.x * self.cell_size + self.cell_size // 2
        old_y = (self.robot.grid_height - 1 - old_pos.y) * self.cell_size + self.cell_size // 2
        new_x = new_pos.x * self.cell_size + self.cell_size // 2
        new_y = (self.robot.grid_height - 1 - new_pos.y) * self.cell_size + self.cell_size // 2
        
        # Animation parameters - match move_delay timing
        steps = 30  # Keep smooth animation with 30 steps
        total_animation_time = move_delay * 1000  # Convert to milliseconds
        delay = int(total_animation_time / steps)  # Calculate delay to match move_delay
        
        print(f"🎬 Animation: {steps} steps, {delay}ms per step, total {total_animation_time}ms (move_delay={move_delay}s)")
        
        dx = (new_x - old_x) / steps
        dy = (new_y - old_y) / steps
        
        def animate_step(step):
            if step <= steps and self.robot_item:
                current_x = old_x + dx * step
                current_y = old_y + dy * step
                
                # Move robot item
                self.canvas.coords(self.robot_item, current_x, current_y)
                
                if step < steps:
                    self.root.after(delay, lambda: animate_step(step + 1))
                else:
                    # Animation complete - ALWAYS draw the trail for this movement
                    print(f"🔴 Animation complete, drawing trail: {old_pos} → {new_pos}")
                    self._draw_trail_segment(old_pos, new_pos)
                    self.animating = False
                    # After finishing this animation, process next queued move if any
                    if self._move_queue:
                        next_old, next_new, next_delay = self._move_queue.pop(0)
                        # Ensure we keep trail order consistent
                        self.animate_move_with_trail(next_old, next_new, next_delay)
        
        animate_step(0)

    def animate_move(self, old_pos: Position, new_pos: Position, move_delay: float = 1.5):
        """Animate smooth movement from old position to new position."""
        if not self.robot_item or self.animating:
            return
        
        self.animating = True
        
        # Calculate canvas coordinates
        old_x = old_pos.x * self.cell_size + self.cell_size // 2
        old_y = (self.robot.grid_height - 1 - old_pos.y) * self.cell_size + self.cell_size // 2
        new_x = new_pos.x * self.cell_size + self.cell_size // 2
        new_y = (self.robot.grid_height - 1 - new_pos.y) * self.cell_size + self.cell_size // 2
        
        # Animation parameters - match move_delay timing
        steps = 30  # Keep smooth animation with 30 steps
        total_animation_time = move_delay * 1000  # Convert to milliseconds
        delay = int(total_animation_time / steps)  # Calculate delay to match move_delay
        
        print(f"🎬 Animation: {steps} steps, {delay}ms per step, total {total_animation_time}ms (move_delay={move_delay}s)")
        
        dx = (new_x - old_x) / steps
        dy = (new_y - old_y) / steps
        
        # Add a small initial delay so trail appears first, then robot follows smoothly
        def start_animation():
            def animate_step(step):
                if step <= steps and self.robot_item:
                    current_x = old_x + dx * step
                    current_y = old_y + dy * step
                    
                    # Move robot item
                    self.canvas.coords(self.robot_item, current_x, current_y)
                    
                    if step < steps:
                        self.root.after(delay, lambda: animate_step(step + 1))
                    else:
                        self.animating = False
            
            animate_step(0)
        
        # Small delay (50ms) so trail draws first, then smooth animation follows
        self.root.after(50, start_animation)
    
    def robot_moved(self, old_pos: Position, new_pos: Position, success: bool, move_delay: float = 1.5):
        """Called when robot attempts to move - handles animation and trail."""
        # Only proceed if canvas is initialized
        if not self.canvas:
            print("⚠️  GUI not yet initialized - skipping visual update")
            return
        
        if success:
            # Make defensive copies so future robot moves don't mutate stored references
            old_copy = Position(old_pos.x, old_pos.y)
            new_copy = Position(new_pos.x, new_pos.y)

            # Record logical trail path (copy)
            self.movement_trail.append(new_copy)

            # If an animation is already running, queue this move
            if self.animating:
                self._move_queue.append((old_copy, new_copy, move_delay))
            else:
                # Start animation that will draw trail after completion
                self.animate_move_with_trail(old_copy, new_copy, move_delay)
        else:
            # Robot hit wall - show popup and auto-reset
            self._handle_wall_collision()
    
    def _draw_trail_segment(self, start_pos: Position, end_pos: Position):
        """Draw a single red trail segment between two positions."""
        # Only draw if positions are different (actual movement occurred)
        if start_pos.x == end_pos.x and start_pos.y == end_pos.y:
            print(f"⚠️  No movement - positions are identical: {start_pos}")
            return
            
        # Convert to canvas coordinates
        start_x = start_pos.x * self.cell_size + self.cell_size // 2
        start_y = (self.robot.grid_height - 1 - start_pos.y) * self.cell_size + self.cell_size // 2
        end_x = end_pos.x * self.cell_size + self.cell_size // 2
        end_y = (self.robot.grid_height - 1 - end_pos.y) * self.cell_size + self.cell_size // 2
        
        # Draw thick red line with enhanced visibility (behind other elements)
        line_item = self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="#ff0000", width=8, capstyle=tk.ROUND, smooth=True, tags="trail"
        )
        
        # Send trail to back so it appears under the robot
        self.canvas.tag_lower(line_item)
        
        # Force canvas update to show line immediately
        self.canvas.update_idletasks()
        
        # Debug print to verify line is being drawn
        print(f"🔴 Drew red line from ({start_x},{start_y}) to ({end_x},{end_y}) - width=8px")
    
    def _handle_wall_collision(self):
        """Handle wall collision with popup and auto-reset."""
        # Show popup message
        messagebox.showwarning(
            "Wall Hit!",
            "🚫 Robot hit a wall!\n\n🔄 Returning to starting position.\n\n⚠️ Simulation stopped. Please fix your code and run again."
        )
        
        # Reset but don't continue execution
        self._reset_robot()
        
        # Stop the current move sequence by raising an exception that will be caught
        raise RuntimeError("Simulation stopped due to wall collision")
    
    def _reset_robot(self):
        """Reset robot to starting position but preserve trail to show path covered."""
        self.robot.reset_simulation()
        
        # Add reset position to trail (to show complete path including reset)
        start_pos = self.robot.get_position()
        self.movement_trail.append(start_pos)
        
        # Redraw scene
        self._draw_complete_scene()
        
        print("🔄 Robot reset to starting position - trail preserved to show full path")
    
    def update_display(self):
        """Update the display after robot state changes."""
        if self.root and self.canvas:
            self._draw_complete_scene()
            self.root.update()
    
    def start_visualization(self, auto_close_seconds: Optional[int] = None):
        """Start the visual simulation."""
        if self.running:
            return
        
        self.running = True
        self._setup_window()
        
        # Set up auto-close if specified
        if auto_close_seconds:
            def auto_close():
                print(f"⏰ Auto-closing simulator after {auto_close_seconds} seconds")
                self._close()
            
            self.root.after(auto_close_seconds * 1000, auto_close)
            print(f"🖥️  Simulator will stay open for {auto_close_seconds} seconds...")
        
        # Start the GUI loop
        try:
            self.root.mainloop()
        except tk.TclError:
            pass
        finally:
            self.running = False
    
    def _close(self):
        """Close the simulator."""
        self.running = False
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass

class RobotProgram:
    """
    Enhanced wrapper for educational robot programming with improved features.
    """
    
    def __init__(self, width: int = 10, height: int = 10, start_x: int = 0, start_y: int = 0):
        # Create robot with 10x10 default grid
        self.robot = Robot(start_x, start_y)
        self.robot.grid_width = width
        self.robot.grid_height = height

        # Defensive: if a wall already exists at the start (e.g., user added before init in custom flow)
        if (start_x, start_y) in getattr(self.robot, 'walls', set()):
            raise ValueError(f"Robot cannot start inside a wall at ({start_x}, {start_y})")
        
        # Create enhanced simulator
        self.simulator = EnhancedSimulator(self.robot)
        
        print(f"📐 Grid size set to {width} x {height}")
        print(f"🤖 Robot Program initialized: {width}x{height} grid")
        print(f"📍 Robot starting position: ({start_x}, {start_y})")
        print("📖 Available commands: robot.move('up'/'down'/'left'/'right'/'backward')")
        print("🔧 Use robot.get_position() to check current location")
        print("⚠️  Simulation stops on illegal moves - use robot.reset_simulation() to continue")
    
    def add_wall(self, x: int, y: int):
        """Add a wall at the specified position."""
        self.robot.add_wall(x, y)
        print(f"🧱 Wall added at ({x}, {y})")
        if hasattr(self, 'simulator'):
            self.simulator.update_display()
    
    def load_maze(self, layout):
        """Load a maze layout."""
        result = self.robot.load_maze(layout)
        if hasattr(self, 'simulator'):
            self.simulator.update_display()
        return result
    
    def start(self):
        """Start the visual simulator."""
        print("🚀 Starting enhanced simulator...")
        self.simulator.start_visualization()
    
    def start_with_auto_close(self, delay_seconds: int = 5):
        """Start simulator and auto-close after specified seconds."""
        print(f"🚀 Starting simulator (will auto-close in {delay_seconds}s)...")
        self.simulator.start_visualization(delay_seconds)
    
    def update_display(self):
        """Update the visual display after robot moves."""
        if hasattr(self, 'simulator'):
            self.simulator.update_display()
    
    def move_with_delay(self, direction: str):
        """Move robot with visual delay and animation (1.5 second delay)."""
        old_pos = Position(self.robot.position.x, self.robot.position.y)  # Capture before move
        success = self.robot.move(direction)
        new_pos = self.robot.get_position()  # Get after move
        
        # Notify simulator about the move
        if hasattr(self, 'simulator') and self.simulator.running:
            self.simulator.robot_moved(old_pos, new_pos, success)
        
        time.sleep(1.5)  # Fixed 1.5 second delay
        return success
