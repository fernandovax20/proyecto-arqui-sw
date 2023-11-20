import os
import platform

def launch_services():
    if platform.system() == "Windows":
        # Lanza los servicios en Windows
        os.system("start cmd /k python services/mainService.py dbcon")
        os.system("start cmd /k python services/mainService.py svses")
        os.system("start cmd /k python services/mainService.py servc")
        os.system("start cmd /k python services/mainService.py userc")
        os.system("start cmd /k python services/mainService.py resec")
        os.system("start cmd /k python services/correo.py")
        os.system("start cmd /k python services/apiCorreos.py")
    else:
        # Lanza los servicios en Linux con gnome-terminal
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py dbcon; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py svses; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py servc; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py userc; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/mainService.py resec; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/correo.py; exec bash'")
        os.system("gnome-terminal -- bash -c 'python3 services/apiCorreos.py; exec bash'")
if __name__ == "__main__":
    launch_services()
