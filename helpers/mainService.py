import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import busConnect as bc
from services import serviceListaServicios as ls
from services import serviceIniciarSesion as inses
from services import serviceRegistrarUsuario as reg
#from services import serviceSesiones as ses
from services import serviceDB as db

def main():
    if sys.argv[1] == "lsbar": # este lanza la lista de los servicios de barberia
        bc.GlobalServiceConnect("lsbar", ls.ListarServicios)

    elif sys.argv[1] == "inses": # Iniciar sesion de usuario
        bc.GlobalServiceConnect("inses", inses.IniciarSesion)

    elif sys.argv[1] == "dbcon": # Conectar a la base de datos
        bc.GlobalServiceConnect("dbcon", db.instruccion)

    #elif sys.argv[1] == "svses": # Verificar sesiones
        #bc.GlobalServiceConnect("svses", ses.instruccion)
    else:
        print("Argumento no válido")

if __name__ == "__main__":
    main()
