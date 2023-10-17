import subprocess

def launch_services():
    # Lanza el servicio de sumar en una nueva ventana de terminal
    subprocess.Popen(["cmd.exe", "/c", "python mainService.py sumar"])
    
    # Lanza el servicio de lista en una nueva ventana de terminal
    subprocess.Popen(["cmd.exe", "/c", "python mainService.py lista"])

    # Lanza el servicio de lsbar en una nueva ventana de terminal
    subprocess.Popen(["cmd.exe", "/c", "python mainService.py lsbar"])

if __name__ == "__main__":
    launch_services()
