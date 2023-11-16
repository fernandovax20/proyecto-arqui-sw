
from helpers import validadores as val
from .menuCliente import menuCliente 
from .menuAdmin import menuAdmin 
import pwinput
import sys

from views import viewLogic as vl

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
                vl.ListarServicios()

            elif opcion == "2":
                email = input("Ingrese email: ")
                while not val.es_email_valido(email):
                    print("Email no válido. Por favor, ingrese un email correcto.")
                    email = input("Ingrese su email: ")
                
                password = pwinput.pwinput("Ingrese password: ")

                res = vl.IniciarSesion(email, password)

                if res["status"] == "success":
                    if res["rol"] == "cliente":
                        print("Bienvenido cliente")
                        menuCliente(res["nombre"], res["rol"], res["token"])
                    elif res["rol"] == "admin":
                        print("Bienvenido administrador")
                        menuAdmin(res["nombre"], res["rol"], res["token"])
                else:
                    print("Error al iniciar sesión:", res["error"])

            elif opcion == "3":
                email = input("Ingrese su email: ")
                while not val.es_email_valido(email):
                    print("Email no válido. Por favor, ingrese un email correcto.")
                    email = input("Ingrese su email: ")

                nombre = input("Ingrese su nombre: ")
                while not val.es_nombre_valido(nombre):
                    print("Nombre no válido. Por favor, ingrese un nombre que contenga solo letras.")
                    nombre = input("Ingrese su nombre: ")

                password = pwinput.pwinput("Ingrese su contraseña: ")

                res = vl.RegistrarUsuario(nombre, email, password)

                if res["status"] == "error":
                    print("Error al registrar usuario:", res["data"])
                else:
                    print(res["data"])

            elif opcion == "4":
                print("Has salido del sistema")
                sys.exit(0)  # Finalizamos la ejecución del programa directamente