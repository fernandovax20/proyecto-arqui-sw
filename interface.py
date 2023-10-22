from services import busConnect as bc
from prettytable import PrettyTable
import time
import re
import pwinput
import sys

def es_email_valido(email):
    """Verifica si un dato es un email válido."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def es_nombre_valido(nombre):
    """Verifica si un dato contiene solo letras y espacios."""
    return all(caracter.isalpha() or caracter.isspace() for caracter in nombre)

def verificar_token(token):
    """Verifica la validez de un token JWT."""
    res_dict = bc.sendToBus("svses", {"instruccion":"verify_token", "token":token})
    if res_dict["status"]:
        return res_dict["data"]["role"], res_dict["data"]["nombre"]
    else:
        return None, res_dict["data"]

def ListarServicios():
    res = bc.sendToBus("lsbar")
    respuesta = res["servicios"]
    
    tabla = PrettyTable()
    tabla.field_names = ["#", "Nombre", "Descripción", "Precio", "Puntos por Servicio"]
    for i, servicio in enumerate(respuesta, start=1):
        tabla.add_row([i, servicio['nombre'], servicio['description'], servicio['precio'], servicio['puntos_por_servicio']])
    print(tabla)
    time.sleep(2)

def IniciarSesion(email, password):
    return bc.sendToBus("inses", {"email": email, "password": password})

def RegistrarUsuario(nombre, email, password):
    return bc.sendToBus("regus", {"nombre": nombre, "email": email, "password": password})

def menuCliente(nombre, rol, token):
    while True:
        print(f"""
        Bienvenido {rol} {nombre}
        1. Reservar una hora
        2. Salir
        \n
        token: {token}
        _________________________________________________________
        """)
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            print("Reservar una hora")
        elif opcion == "2":
            print("Has salido del menú cliente")
            return


def menuAdmin(nombre, rol, token):
    while True:
        print(f"""
        Bienvenido {rol} {nombre}
        1. Administrar Servicios
        2. Administrar Usuarios
        3. Salir
        \n
        token: {token}
        _________________________________________________________
        """)
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            print("Administrar Servicios")
        elif opcion == "2":
            print("Administrar Usuarios")
        elif opcion == "3":
            print("Has salido del menú administrador")
            return

def menuPrincipal():
    while True:
            print("""
            Bienvenido a Barber House
            1. Listar Servicios de Barbería
            2. Iniciar Sesión
            3. Registrarse
            4. Salir
            \n
            _________________________________________________________
            """)
            opcion = input("Ingrese opción: ")

            if opcion == "1":
                ListarServicios()

            elif opcion == "2":
                email = input("Ingrese email: ")
                while not es_email_valido(email):
                    print("Email no válido. Por favor, ingrese un email correcto.")
                    email = input("Ingrese su email: ")
                
                password = pwinput.pwinput("Ingrese password: ")

                res = IniciarSesion(email, password)

                if res["status"] == "success":
                    if res["rol"] == "cliente":
                        menuCliente(res["nombre"], res["rol"], res["token"])
                    elif res["rol"] == "admin":
                        menuAdmin(res["nombre"], res["rol"], res["token"])
                else:
                    print("Error al iniciar sesión:", res["error"])

            elif opcion == "3":
                email = input("Ingrese su email: ")
                while not es_email_valido(email):
                    print("Email no válido. Por favor, ingrese un email correcto.")
                    email = input("Ingrese su email: ")

                nombre = input("Ingrese su nombre: ")
                while not es_nombre_valido(nombre):
                    print("Nombre no válido. Por favor, ingrese un nombre que contenga solo letras.")
                    nombre = input("Ingrese su nombre: ")

                password = pwinput.pwinput("Ingrese su contraseña: ")

                res = RegistrarUsuario(nombre, email, password)

                if res["status"] == "error":
                    print("Error al registrar usuario:", res["data"])
                else:
                    print(res["data"])

            elif opcion == "4":
                print("Has salido del sistema")
                sys.exit(0)  # Finalizamos la ejecución del programa directamente

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        rol, mensaje = verificar_token(token)

        if rol:
            if rol == "cliente":
                menuCliente(mensaje, rol, token)
            elif rol == "admin":
                menuAdmin(mensaje, rol, token)
            # Llamar al menú principal después de salir de menuCliente o menuAdmin
            menuPrincipal()
        else:
            print("Error:", mensaje)
            menuPrincipal()
    else:
        menuPrincipal()

