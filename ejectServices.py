import os
import platform

def launch_services():
    if platform.system() == "Windows":
        # Lanza los servicios en Windows
        os.system("start cmd /k python services/mainService.py lsbar")
        os.system("start cmd /k python services/mainService.py inses")
        os.system("start cmd /k python services/mainService.py dbcon")
        os.system("start cmd /k python services/mainService.py svses")
        os.system("start cmd /k python services/mainService.py regus")
    else:
        # Lanza los servicios en Linux con gnome-terminal
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py lsbar; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py inses; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py dbcon; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py svses; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py regus; exec bash'")
if __name__ == "__main__":
    launch_services()
