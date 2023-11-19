from helpers import validadores as val
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

                email = val.obtener_email_valido()
                password = pwinput.pwinput("Ingrese password: ")

                vl.IniciarSesion(email, password)

            elif opcion == "3":

                email = val.obtener_email_valido()
                nombre = val.obtener_nombre_valido()
                password = pwinput.pwinput("Ingrese su contraseña: ")

                vl.RegistrarUsuario(nombre, email, password)

            elif opcion == "4":
                print("Has salido del sistema")
                sys.exit(0)  # Finalizamos la ejecución del programa directamente