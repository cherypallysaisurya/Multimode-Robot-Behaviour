#!/usr/bin/env python3
"""Developer helper to show which robot_behavior package is imported."""
import importlib, sys, inspect

def main():
    try:
        rb = importlib.import_module("robot_behavior")
        path = inspect.getfile(rb)
        print(f"robot_behavior imported from: {path}")
        print(f"version: {getattr(rb,'__version__','<no __version__>')}")
        print(f"module file directory: {rb.__path__}")
    except Exception as e:
        print("Failed to import robot_behavior:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
