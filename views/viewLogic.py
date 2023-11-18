from services import busConnect as bc
from prettytable import PrettyTable
import time
from .menuCliente import menuCliente 
from .menuAdmin import menuAdmin 

##############################################################################################
# Servicios
def ListarServicios():
    try:
        res = bc.sendToBus("servc", {"instruccion": "ListarServicios"})
        respuesta = res["servicios"]
        
        ids_servicios = []  

        tabla = PrettyTable()
        tabla.field_names = ["#", "Nombre", "Precio", "Puntos por Servicio"]
        for i, servicio in enumerate(respuesta, start=1):
            tabla.add_row([servicio["id"], servicio['nombre'], servicio['precio'], servicio['puntos_por_servicio']])
            ids_servicios.append(servicio["id"]) 
        print(tabla)
        time.sleep(2)
        return ids_servicios
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def CrearServicio(token,nombre, precio, puntos_por_servicio):
    try:
        res = bc.sendToBus("servc", 
            {"instruccion": "CrearServicio", 
                "token":token,
                "nombre": nombre, 
                "precio": precio, 
                "puntos_por_servicio": puntos_por_servicio})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def editarServicio(token, id, nombre, precio, puntos_por_servicio):
    try:
        res = bc.sendToBus("servc", 
            {"instruccion": "EditarServicio", 
                "token":token,
                "id": id,
                "nombre": nombre, 
                "precio": precio, 
                "puntos_por_servicio": puntos_por_servicio})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def eliminarServicio(token, id):
    try:
        res = bc.sendToBus("servc", 
            {"instruccion": "EliminarServicio", 
                "token":token,
                "id": id})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

##############################################################################################
# Usuarios
def IniciarSesion(email, password):
    try:
        res = bc.sendToBus("inses", {"email": email, "password": password})
        if res["status"] == "success":
            if res["rol"] == "cliente":
                print("Bienvenido cliente")
                menuCliente(res["nombre"], res["rol"], res["token"])
            elif res["rol"] == "admin":
                print("Bienvenido administrador")
                menuAdmin(res["nombre"], res["rol"], res["token"])
        else:
            print("Error al iniciar sesión:", res["data"])
    except Exception:
        print(f"Ocurrió un error al iniciar sesion o en la sesion, porfavor intente mas tarde")
    

def RegistrarUsuario(nombre, email, password):
    try:
        res = bc.sendToBus("regus", {"nombre": nombre, "email": email, "password": password})
        if res["status"] == "error":
            print("Error al registrar usuario:", res["data"])
        else:
            print("Error al registrar usuario",res["data"])
    except Exception :
        print(f"Ocurrió un error al registar el usuario, porfavor intente mas tarde")


