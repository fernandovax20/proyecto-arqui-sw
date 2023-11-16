from services import busConnect as bc
from prettytable import PrettyTable
import time

##############################################################################################
# Servicios
def ListarServicios():
    res = bc.sendToBus("servc", {"instruccion": "ListarServicios"})
    respuesta = res["servicios"]
    
    tabla = PrettyTable()
    tabla.field_names = ["#", "Nombre", "Precio", "Puntos por Servicio"]
    for i, servicio in enumerate(respuesta, start=1):
        tabla.add_row([servicio["id"], servicio['nombre'], servicio['precio'], servicio['puntos_por_servicio']])
    print(tabla)
    time.sleep(2)

def CrearServicio(token,nombre, description, precio, duracion, puntos_por_servicio):
    res = bc.sendToBus("servc", 
        {"instruccion": "CrearServicio", 
            "token":token,
            "nombre": nombre, 
            "description": description, 
            "precio": precio, 
            "duracion": duracion, 
            "puntos_por_servicio": puntos_por_servicio})
    return res

def eliminarServicio(token, id):
    res = bc.sendToBus("servc", 
        {"instruccion": "EliminarServicio", 
            "token":token,
            "id": id})
    return res

def IniciarSesion(email, password):
    return bc.sendToBus("inses", {"email": email, "password": password})

def RegistrarUsuario(nombre, email, password):
    return bc.sendToBus("regus", {"nombre": nombre, "email": email, "password": password})