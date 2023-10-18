from helpers import busConnect as bc
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
    print(res)
    
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
            print("_________________________________________________________")