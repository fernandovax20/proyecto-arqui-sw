from services import busConnect as bc
from prettytable import PrettyTable
import time

def ListarServicios(data=None):
    res = bc.sendToBus("lsbar")  # Asumiendo que esto retorna el JSON mencionado
    respuesta = res["servicios"]
    
    tabla = PrettyTable() # Crear una tabla con prettytable
   
    tabla.field_names = ["#", "Nombre", "Descripción", "Precio", "Puntos por Servicio"] # Definir los encabezados de la tabla
    
    for i, servicio in enumerate(respuesta, start=1):# Iterar sobre los servicios y agregar cada uno como una fila en la tabla
        tabla.add_row([i, servicio['nombre'], servicio['description'], servicio['precio'], servicio['puntos_por_servicio']])
    
    print(tabla)# Imprimir la tabla
    time.sleep(2)

def IniciarSesion(email, password):
    data = {
        "email": email,
        "password": password
    }
    res = bc.sendToBus("inses", data)
    usuario = res["user"]
    print(usuario, type(usuario))
    print(usuario['status'])
    print(usuario['data']['nombre'], 
          usuario['data']['email'],
          usuario['data']['nombre_rol'],
          res['token']
    )
    #print(res["status"], type(res))

def menuCliente(nombre, rol, token):
    salir = False
    while(not salir):
        print(f"""
        Bienvenido {rol} {nombre}\n
        1. Reservar una hora\n
        2. Salir\n
        _________________________________________________________\n
        """)
        opcion = input("Ingrese opción: ")
        print("\n")

        if(opcion == "1"):
            print("Reservar una hora")

        elif(opcion == "2"):
            salir = True
            print("_________________________________________________________")

def menuAdmin(nombre, rol, token):
    salir = False
    while(not salir):
        print(f"""
        Bienvenido {rol} {nombre}\n
        1. Administrar Servicios\n
        2. Administrar Usuarios\n
        3. Salir\n
        _________________________________________________________\n
        """)
        opcion = input("Ingrese opción: ")
        print("\n")

        if(opcion == "1"):
            print("Administrar Servicios")

        elif(opcion == "2"):
            print("Administrar Usuarios")

        elif(opcion == "3"):
            salir = True
            print("_________________________________________________________")
    
if __name__ == "__main__":
    salir = False
    while(not salir):
        print("""
        Bienvenido a Barber House\n
        1. Listar Servicios de Barbería\n
        2. Iniciar Sesión\n
        3. Registrarse\n
        4. Salir\n
        _________________________________________________________\n
        """)
        opcion = input("Ingrese opción: ")
        print("\n")

        if(opcion == "1"):
            ListarServicios()

        elif(opcion == "2"):
            print("Iniciar Sesión")
            email = input("Ingrese email: ")
            password = input("Ingrese password: ")

            IniciarSesion(email, password)

        elif(opcion == "3"):
            print("Registrarse")
        elif(opcion == "4"):
            salir = True
            print(" Has salido del sistema ")
            print("_________________________________________________________")

            