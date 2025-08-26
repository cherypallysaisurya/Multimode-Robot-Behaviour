from robot_behavior.minimal_api import create_robot_program, run_with_visualization

def speed_demo():
    """Demo showing different robot movement speeds"""
    
    print("🐌 Robot Movement Speed Demo")
    print("=" * 40)
    
    # Create robot world
    program = create_robot_program(5, 5, 0, 1)
    program.add_wall(2, 0)
    program.add_wall(3, 1)
    
    # Define robot movements
    def my_moves():
        program.robot.move('right')
        program.robot.move('right') 
        program.robot.move('up')
        program.robot.move('up')
    
    # Run with custom speed (1.5 seconds between moves)
    print("🚀 Running with moderate speed (1.5s delay)...")
    run_with_visualization(program, my_moves, move_delay=1.5)

def fast_demo():
    """Demo with faster robot movement"""
    
    print("⚡ Fast Robot Demo")
    print("=" * 20)
    
    program = create_robot_program(6, 6, 0, 0)
    program.add_wall(2, 1)
    program.add_wall(3, 2)
    
    def fast_moves():
        program.robot.move('right')
        program.robot.move('right')
        program.robot.move('up')
        program.robot.move('up')
        program.robot.move('right')
        program.robot.move('up')
    
    # Faster movement (0.8 seconds between moves)
    run_with_visualization(program, fast_moves, move_delay=0.8)

def slow_demo():
    """Demo with slower robot movement"""
    
    print("🐌 Slow Robot Demo")
    print("=" * 20)
    
    program = create_robot_program(4, 4, 0, 0)
    
    def slow_moves():
        program.robot.move('right')
        program.robot.move('up')
        program.robot.move('right')
        program.robot.move('up')
    
    # Slower movement (2.5 seconds between moves)
    run_with_visualization(program, slow_moves, move_delay=2.5)

if __name__ == "__main__":
    # Run the moderate speed demo by default
    speed_demo()
    
    # Uncomment to try other speeds:
    # fast_demo()     # ⚡ Fast: 0.8s delay
    # slow_demo()     # 🐌 Slow: 2.5s delay
