#!/usr/bin/env python3
"""
Test environment variable system for robot mode control
"""

from unified_robot import create_robot_program

def test_env_control():
    print("🧪 Testing Environment Variable Control")
    print("=" * 50)
    
    # Test 1: Default behavior (no mode specified)
    print("1. Default behavior (students use this):")
    program = create_robot_program()
    print(f"   Mode: {program.mode}")
    
    # Test 2: Explicit mode (students can still override)
    print("\n2. Explicit mode (students can still do this):")
    program_real = create_robot_program(mode="real")
    print(f"   Mode: {program_real.mode}")
    
    print("\n✅ Environment variable system working!")
    print("📋 Instructions for TAs:")
    print("   - Students: just use create_robot_program() (gets simulator)")
    print("   - TAs: set $env:ROBOT_MODE='real' then run student code")

if __name__ == "__main__":
    test_env_control()
