from services import busConnect as bc
from prettytable import PrettyTable
import time
import re
import pwinput

def es_email_valido(email):
    """Verifica si un dato es un email válido."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def es_nombre_valido(nombre):
    """Verifica si un dato contiene solo letras y espacios."""
    return all(caracter.isalpha() or caracter.isspace() for caracter in nombre)




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
    return res

def RegistrarUsuario(nombre, email, password):
    data = {
        "nombre": nombre,
        "email": email,
        "password": password
    }
    res = bc.sendToBus("regus", data)
    print(res)
    return res

def menuCliente(nombre, rol, token):
    salir = False
    while(not salir):
        print(f"""
        Bienvenido {rol} {nombre}\n
        1. Reservar una hora\n
        2. Salir\n
        \n
        token: {token}
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
        \n
        token: {token}
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
            password = pwinput.pwinput("Ingrese password: ")

            res = IniciarSesion(email, password)

            if(res["status"] == "success"):
                if (res["rol"] == "cliente"):
                    menuCliente(res["nombre"], res["rol"], res["token"])
                elif (res["rol"] == "admin"):
                    menuAdmin(res["nombre"], res["rol"], res["token"])
            else:
                print("Error al iniciar sesión")
                print(res["error"])

        elif(opcion == "3"):
            print("Registrarse")

            # Solicitar email hasta que sea válido
            email = input("Ingrese su email: ")
            while not es_email_valido(email):
                print("Email no válido. Por favor, ingrese un email correcto.")
                email = input("Ingrese su email: ")
                
            # Solicitar nombre hasta que sea válido
            nombre = input("Ingrese su nombre: ")
            while not es_nombre_valido(nombre):
                print("Nombre no válido. Por favor, ingrese un nombre que contenga solo letras.")
                nombre = input("Ingrese su nombre: ")
                
            # Solicitar contraseña (puedes añadir más validaciones si lo deseas)
            password = pwinput.pwinput("Ingrese su contraseña: ")

            res = RegistrarUsuario(nombre, email, password)

            if(res["status"] == "error"):
                print("Error al registrar usuario")
                print(res["data"])
            else:
                print(res["data"])

        elif(opcion == "4"):
            salir = True
            print(" Has salido del sistema ")
            print("_________________________________________________________")

            