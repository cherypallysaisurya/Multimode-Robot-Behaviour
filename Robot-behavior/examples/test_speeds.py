from robot_behavior.minimal_api import create_robot_program, run_fast, run_normal, run_slow

def test_speed_options():
    """Test different speed options"""
    
    print("🚀 Testing Fast Speed (0.5s delay)")
    program = create_robot_program(4, 4, 0, 0)
    
    def fast_moves():
        program.robot.move('right')
        program.robot.move('up')
        program.robot.move('right')
    
    run_fast(program, fast_moves)

def test_normal_speed():
    """Test normal speed"""
    
    print("⚡ Testing Normal Speed (1.0s delay)")
    program = create_robot_program(4, 4, 0, 0)
    
    def normal_moves():
        program.robot.move('right')
        program.robot.move('up')
        program.robot.move('right')
    
    run_normal(program, normal_moves)

def test_slow_speed():
    """Test slow speed"""
    
    print("🐌 Testing Slow Speed (2.5s delay)")
    program = create_robot_program(4, 4, 0, 0)
    
    def slow_moves():
        program.robot.move('right')
        program.robot.move('up')
        program.robot.move('right')
    
    run_slow(program, slow_moves)

if __name__ == "__main__":
    # Test fast speed by default
    test_speed_options()
    
    # Uncomment to test other speeds:
    # test_normal_speed()
    # test_slow_speed()
