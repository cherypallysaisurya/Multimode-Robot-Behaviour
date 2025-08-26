#!/usr/bin/env python3
"""
🚀 Robot Behavior Simulator - Build & Package Script

This script handles the complete build, test, and packaging workflow
for the robot-behavior-simulator package.

Usage:
    python scripts/build_package.py [command]

Commands:
    clean       - Clean build artifacts
    test        - Run all tests
    build       - Build the package
    check       - Check package integrity
    upload-test - Upload to TestPyPI
    upload      - Upload to PyPI
    all         - Run complete pipeline (clean, test, build, check)

Requirements:
    - Python 3.7+
    - build, twine, pytest packages
    - Valid PyPI credentials for upload
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

class PackageBuilder:
    """Handles building and packaging the robot-behavior-simulator."""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.dist_dir = self.root_dir / "dist"
        self.build_dir = self.root_dir / "build"
        self.egg_info_dirs = list(self.root_dir.glob("*.egg-info"))
        
    def print_banner(self, message):
        """Print a formatted banner message."""
        print("\n" + "="*60)
        print(f"🤖 {message}")
        print("="*60)
        
    def run_command(self, command, description):
        """Run a shell command with error handling."""
        self.print_banner(description)
        print(f"Running: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command, 
                cwd=self.root_dir,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False
    
    def clean(self):
        """Clean all build artifacts."""
        self.print_banner("Cleaning build artifacts")
        
        # Directories to remove
        dirs_to_remove = [
            self.dist_dir,
            self.build_dir,
            *self.egg_info_dirs,
            self.root_dir / "__pycache__",
            self.root_dir / "robot_behavior" / "__pycache__",
            self.root_dir / ".pytest_cache",
            self.root_dir / "htmlcov",
        ]
        
        for dir_path in dirs_to_remove:
            if dir_path.exists():
                print(f"🗑️  Removing {dir_path}")
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f"⚠️  Could not remove {dir_path}: {e}")
            
        # Files to remove
        files_to_remove = [
            self.root_dir / ".coverage",
        ]
        
        for file_path in files_to_remove:
            if file_path.exists():
                print(f"🗑️  Removing {file_path}")
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"⚠️  Could not remove {file_path}: {e}")
                
        print("✅ Clean complete")
        return True
        
    def test(self):
        """Run all tests."""
        self.print_banner("Running tests")
        
        # Check if pytest is available
        try:
            import pytest
        except ImportError:
            print("⚠️  pytest not installed, installing...")
            if not self.run_command([sys.executable, "-m", "pip", "install", "pytest"], "Installing pytest"):
                return False
        
        # Run tests
        test_command = [sys.executable, "-m", "pytest", "tests/", "-v"]
        if not self.run_command(test_command, "Running pytest"):
            return False
            
        print("✅ All tests passed")
        return True
        
    def build(self):
        """Build the package."""
        self.print_banner("Building package")
        
        # Check if build is available
        try:
            import build
        except ImportError:
            print("⚠️  build not installed, installing...")
            if not self.run_command([sys.executable, "-m", "pip", "install", "build"], "Installing build"):
                return False
        
        # Build the package
        build_command = [sys.executable, "-m", "build"]
        if not self.run_command(build_command, "Building package"):
            return False
            
        # List built files
        if self.dist_dir.exists():
            print("\n📦 Built packages:")
            for file in self.dist_dir.iterdir():
                print(f"  • {file.name} ({file.stat().st_size} bytes)")
                
        print("✅ Build complete")
        return True
        
    def check(self):
        """Check package integrity."""
        self.print_banner("Checking package integrity")
        
        # Check if twine is available
        try:
            import twine
        except ImportError:
            print("⚠️  twine not installed, installing...")
            if not self.run_command([sys.executable, "-m", "pip", "install", "twine"], "Installing twine"):
                return False
        
        # Check package
        check_command = [sys.executable, "-m", "twine", "check", "dist/*"]
        if not self.run_command(check_command, "Checking package with twine"):
            return False
            
        print("✅ Package check passed")
        return True
        
    def upload_test(self):
        """Upload to TestPyPI."""
        self.print_banner("Uploading to TestPyPI")
        
        upload_command = [
            sys.executable, "-m", "twine", "upload",
            "--repository", "testpypi",
            "dist/*"
        ]
        
        if not self.run_command(upload_command, "Uploading to TestPyPI"):
            return False
            
        print("✅ Upload to TestPyPI complete")
        print("🔗 Check: https://test.pypi.org/project/robot-behavior-simulator/")
        return True
        
    def upload(self):
        """Upload to PyPI."""
        self.print_banner("Uploading to PyPI")
        
        # Confirm upload
        response = input("⚠️  This will upload to PyPI. Continue? (y/N): ")
        if response.lower() != 'y':
            print("❌ Upload cancelled")
            return False
        
        upload_command = [sys.executable, "-m", "twine", "upload", "dist/*"]
        
        if not self.run_command(upload_command, "Uploading to PyPI"):
            return False
            
        print("✅ Upload to PyPI complete")
        print("🔗 Check: https://pypi.org/project/robot-behavior-simulator/")
        return True
        
    def run_all(self):
        """Run complete build pipeline."""
        self.print_banner("Running complete build pipeline")
        
        steps = [
            ("clean", self.clean),
            ("test", self.test), 
            ("build", self.build),
            ("check", self.check),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"❌ Pipeline failed at step: {step_name}")
                return False
                
        print("\n🎉 Complete pipeline successful!")
        print("📦 Package ready for upload")
        print("🚀 Use 'upload-test' or 'upload' to publish")
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Robot Behavior Simulator build script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build_package.py clean     # Clean build artifacts
  python scripts/build_package.py test      # Run tests only
  python scripts/build_package.py all       # Complete pipeline
  python scripts/build_package.py build     # Build package only
        """
    )
    
    parser.add_argument(
        "command",
        choices=["clean", "test", "build", "check", "upload-test", "upload", "all"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    builder = PackageBuilder()
    
    # Command mapping
    commands = {
        "clean": builder.clean,
        "test": builder.test,
        "build": builder.build, 
        "check": builder.check,
        "upload-test": builder.upload_test,
        "upload": builder.upload,
        "all": builder.run_all,
    }
    
    # Execute command
    success = commands[args.command]()
    
    if success:
        print("\n✅ Command completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Command failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
