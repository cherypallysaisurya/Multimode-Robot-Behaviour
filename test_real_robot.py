#!/usr/bin/env python3

from unified_robot import create_robot_program, run_with_visualization

def safe_robot_test():
    
    program = create_robot_program(mode="real")
    
    def minimal_moves():
        program.robot.move("up") 
        program.robot.move("down")     # Forward
         
    
    run_with_visualization(program, minimal_moves, move_delay=1.0)  
    
    print("✅ Robot test completed!")


if __name__ == "__main__":
  
    response = input("🚨 SAFETY CHECK: Is robot area clear? (y/N): ")
    if response.lower() == 'y':
        safe_robot_test()
    else:
        print("❌ Test cancelled for safety")
