#!/usr/bin/env python3
"""Create a .pth file in current interpreter site-packages pointing to project root.
Run: python scripts/dev_enable_local_import.py
This is a fallback when editable install is blocked (multiple egg-info issue)."""
import site, sys, os
from pathlib import Path

def main():
    proj_root = Path(__file__).parent.parent.resolve()
    candidates = []
    # Gather site-packages dirs
    for sp in site.getsitepackages()+[site.getusersitepackages()]:
        if os.path.isdir(sp):
            candidates.append(Path(sp))
    if not candidates:
        print('No site-packages dirs found.')
        sys.exit(1)
    target = candidates[0]/'robot_behavior_local_dev.pth'
    target.write_text(str(proj_root)+'\n', encoding='utf-8')
    print('Wrote', target)
    print('Now "import robot_behavior" should resolve to', proj_root)

if __name__ == '__main__':
    main()
