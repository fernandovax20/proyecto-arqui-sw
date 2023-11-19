import sys
import busConnect as bc
import serviceSesiones as ses
import serviceDB as db
import serviceCRUDservicios as servcrud
import serviceCRUDusuarios as usercrud
import serviceCRUDreservas as reservascrud

def main():

    if sys.argv[1] == "servc": # CRUD Servicios
        bc.GlobalServiceConnect("servc", servcrud.instruccion)

    elif sys.argv[1] == "userc": #CRUD Usuarios
        bc.GlobalServiceConnect("userc", usercrud.instruccion)

    elif sys.argv[1] == "resec": # CRUD Reservas
        bc.GlobalServiceConnect("resec", reservascrud.instruccion)

    elif sys.argv[1] == "dbcon": # Conectar a la base de datos
        bc.GlobalServiceConnect("dbcon", db.instruccion)

    elif sys.argv[1] == "svses": # Verificar sesiones
        bc.GlobalServiceConnect("svses", ses.instruccion)

    else:
        print("Argumento no válido")

if __name__ == "__main__":
    main()
