import subprocess

def launch_services():
    
    # Lanza el servicio de lsbar en una nueva ventana de terminal
    subprocess.Popen(["cmd.exe", "/c", "python helpers/mainService.py lsbar"])

    # Lanza el servicio de inses en una nueva ventana de terminal
    subprocess.Popen(["cmd.exe", "/c", "python helpers/mainService.py inses"])

    # Lanza el servicio de dbcon en una nueva ventana de terminal
    subprocess.Popen(["cmd.exe", "/c", "python helpers/mainService.py dbcon"])

if __name__ == "__main__":
    launch_services()
