#!/usr/bin/env python3
"""
Real Robot Connection Test
=========================

Run this to test real robot connection before using in assignments.
"""

def test_real_robot():
    print("🤖 REAL ROBOT CONNECTION TEST")
    print("=" * 40)
    
    # Test 1: Check environment
    import os
    robot_mode = os.getenv('ROBOT_MODE', 'simulator')
    print(f"📊 Environment ROBOT_MODE: {robot_mode}")
    
    # Test 2: Test connection
    print("\n🔌 Testing robot connection...")
    
    from unified_robot_control import create_robot_program
    
    try:
        # Force real robot mode for test
        program = create_robot_program(mode="real")
        
        if "MOCK" in str(type(program.robot._dog)):
            print("❌ Robot not connected - using mock mode")
            print("   Solutions:")
            print("   1. Check robot is powered on")
            print("   2. Connect to robot's WiFi network")
            print("   3. Verify: ping 192.168.12.1")
            print("   4. Install: pip install unified-robot-control[hardware]")
        else:
            print("✅ Real robot connected successfully!")
            print("🎯 Ready to run student assignments")
            
            # Test basic movement
            print("\n🧪 Testing basic movement...")
            program.robot.move("right")
            print("✅ Movement test completed")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Check network connection to robot")

if __name__ == "__main__":
    test_real_robot()
