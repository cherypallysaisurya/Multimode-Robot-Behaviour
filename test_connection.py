#!/usr/bin/env python3
"""
Connection Test Only - No Movement
"""

from unified_robot import create_robot_program

def test_connection_only():
    """Test robot connection without any movement"""
    print("🔌 Testing robot connection...")
    
    try:
        program = create_robot_program(mode="real")
        print("✅ Connection successful!")
        print("🤖 Robot is ready for commands")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection_only()
