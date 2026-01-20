import subprocess
import sys
import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).parent.resolve()
VENV_PY = sys.executable  # usa el python activo

def check_requirements():
    req = BASE_DIR / "requirements.txt"
    if not req.exists():
        print("Requirements.txt no encontrado")
        return

    print("Comprobando dependencias...")
    subprocess.check_call(
        [VENV_PY, "-m", "pip", "install", "-r", str(req)],
        #stdout=subprocess.DEVNULL,
        #stderr=subprocess.DEVNULL,
    )

def run_main():
    print("Ejecutando main.py")
    subprocess.Popen([VENV_PY, str(BASE_DIR / "backend.py")])

def run_dashboard():
    subprocess.Popen(
        [VENV_PY, "-m", "streamlit", "run", str(BASE_DIR / "dashboard.py")],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

if __name__ == "__main__":
    check_requirements()
    run_main()
    time.sleep(2)
    run_dashboard()
