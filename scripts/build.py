import os
import sys
import subprocess

def main():
    is_windows = sys.platform.startswith("win")

    icon_path = os.path.join("assets", "icons", "LogoBlackWire.png")

    if is_windows:
        add_data = "assets;assets"
    else:
        add_data = "assets:assets"

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--add-data={add_data}",
        f"--icon={icon_path}",
        "main.py"
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()