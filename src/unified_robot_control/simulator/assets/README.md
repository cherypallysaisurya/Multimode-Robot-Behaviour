# Assets Folder

This folder contains image assets for the Robot Behavior Framework.

## Dog Image

Place your dog PNG file here with the name `dog.png` to replace the default robot triangle with a dog image.

### Requirements:
- **File name**: `dog.png`
- **Format**: PNG (recommended for transparency)
- **Size**: Any size (will be automatically resized to fit grid cells)
- **Recommended**: Square aspect ratio works best

### Example:
```
assets/
  └── dog.png  ← Your dog image goes here
```

### Usage:
Once you place `dog.png` in this folder, the robot will automatically display as a dog image instead of a blue triangle. A small red arrow will indicate the dog's facing direction.

### Installation:
Make sure you have Pillow installed:
```bash
pip install Pillow
```

Or install all requirements:
```bash
pip install -r requirements.txt
```
