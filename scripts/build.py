import os
import sys
import subprocess
from pathlib import Path

def main():
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    is_windows = sys.platform.startswith("win")

    if is_windows:
        icon_path = project_root / "assets" / "icons" / "LogoBlackWire.ico"
    else:
        icon_path = project_root / "assets" / "icons" / "LogoBlackWire.png"

    sep = ";" if is_windows else ":"
    add_data = f"{project_root / 'assets'}{sep}assets"

    cmd = [
        sys.executable, "-m", "PyInstaller",
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