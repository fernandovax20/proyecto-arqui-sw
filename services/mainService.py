import sys
import busConnect as bc
import serviceListaServicios as ls
import serviceIniciarSesion as inses
import serviceRegistrarUsuario as reg
import serviceSesiones as ses
import serviceDB as db

def main():
    if sys.argv[1] == "lsbar": # este lanza la lista de los servicios de barberia
        bc.GlobalServiceConnect("lsbar", ls.ListarServicios)

    elif sys.argv[1] == "inses": # Iniciar sesion de usuario
        bc.GlobalServiceConnect("inses", inses.IniciarSesion)

    elif sys.argv[1] == "dbcon": # Conectar a la base de datos
        bc.GlobalServiceConnect("dbcon", db.instruccion)

    elif sys.argv[1] == "svses": # Verificar sesiones
        bc.GlobalServiceConnect("svses", ses.instruccion)
    else:
        print("Argumento no válido")

if __name__ == "__main__":
    main()
