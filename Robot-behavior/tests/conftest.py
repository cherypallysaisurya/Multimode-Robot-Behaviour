#!/usr/bin/env python3
"""
Test configuration for robot-behavior-simulator tests.
"""

import sys
import os

# Add parent directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test configuration
collect_ignore = ["setup.py"]
