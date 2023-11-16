import json
import busConnect as bc

def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data)
    
    func_map = {
        "ListarServicios": lambda: ListarServicios(),
        "CrearServicio": lambda: crearServicio(datos["token"], datos["nombre"], datos["description"], datos["precio"], datos["duracion"], datos["puntos_por_servicio"]),
        "EditarServicio": lambda: editarServicio(datos["token"], datos["nombre"], datos["description"], datos["precio"], datos["duracion"], datos["puntos_por_servicio"]),
        "EliminarServicio": lambda: eliminarServicio(datos["token"], datos['id'])
    }

    func = func_map.get(datos["instruccion"])
    return func() if func else json.dumps({"status": False, "data": "Instrucción no reconocida"})

def ListarServicios():
    response = bc.sendToBus("dbcon", {"instruccion": "getAllServicios"})
    return json.dumps(response)

def crearServicio(token, nombre, description, precio, duracion, puntos_por_servicio):

    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
    
    response = bc.sendToBus("dbcon", 
        {"instruccion": "createServicio", 
            "nombre": nombre, 
            "description": description, 
            "precio": precio, 
            "duracion": duracion, 
            "puntos_por_servicio": puntos_por_servicio
        }
    )

    return json.dumps(response)

def editarServicio(token, id, nombre, description, precio, duracion, puntos_por_servicio):
    response = bc.sendToBus("dbcon", {"instruccion": "updateServicio"})
    return json.dumps(response)

def eliminarServicio(token, id):
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
    
    response = bc.sendToBus("dbcon", {"instruccion": "deleteServicio", "id": id})
    return json.dumps(response)