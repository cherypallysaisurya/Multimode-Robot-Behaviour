#!/usr/bin/env python3
"""
TestPyPI Upload Instructions
===========================

Follow these steps to upload to TestPyPI for testing:

1. **Register on TestPyPI** (if not done):
   - Go to: https://test.pypi.org/account/register/
   - Create account and verify email

2. **Create API Token**:
   - Go to: https://test.pypi.org/manage/account/#api-tokens
   - Create token with name "unified-robot-control"
   - Copy the token (starts with pypi-...)

3. **Configure twine**:
   ```bash
   # Set environment variable (replace with your token)
   set TWINE_USERNAME=__token__
   set TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmc...your-token-here
   ```

4. **Upload to TestPyPI**:
   ```bash
   # Upload built package
   python -m twine upload --repository testpypi dist/*
   ```

5. **Test Installation from TestPyPI**:
   ```bash
   # Install from TestPyPI
   pip install --index-url https://test.pypi.org/simple/ unified-robot-control
   
   # Test it works
   python -c "from unified_robot_control import create_robot_program; print('Success!')"
   ```

6. **For Real PyPI** (when ready):
   ```bash
   # Upload to real PyPI
   python -m twine upload dist/*
   ```

Files ready for upload:
- unified_robot_control-1.0.0-py3-none-any.whl
- unified_robot_control-1.0.0.tar.gz

Package Features:
✅ Proper src/ layout for PyPI
✅ Environment variable control (ROBOT_MODE)
✅ Hidden go1_py dependency in [hardware] extras
✅ Student-friendly API
✅ Complete documentation
✅ Examples included
"""

if __name__ == "__main__":
    print(__doc__)
