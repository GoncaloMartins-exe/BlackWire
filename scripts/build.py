import os
import sys
import subprocess
from pathlib import Path

def main():
    # garante que estamos na raiz do projeto (onde está o main.py)
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    is_windows = sys.platform.startswith("win")

    icon_path = project_root / "assets" / "icons" / "LogoBlackWire.png"

    if is_windows:
        add_data = f"assets;assets"
    else:
        add_data = f"assets:assets"

    cmd = [
        "pyinstaller",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", "BlackWire",
        f"--add-data={add_data}",
        f"--icon={icon_path}",
        "main.py"
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()