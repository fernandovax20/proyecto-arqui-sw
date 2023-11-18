import json
import busConnect as bc


def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data)
    
    func_map = {
        "ListarUsuarios": lambda: ListarUsuarios(),
        "CrearUsuario": lambda: crearUsuario(datos["token"], datos["nombre"], datos["email"], datos["password"], datos["role"]),
        "EditarUsuario": lambda: editarUsuario(datos["token"],datos['id'], datos["nombre"], datos["email"], datos["password"], datos["role"]),
        "EliminarUsuario": lambda: eliminarUsuario(datos["token"], datos['id'])
    }

    func = func_map.get(datos["instruccion"])
    return func() if func else json.dumps({"status": False, "data": "Instrucción no reconocida"})

def ListarUsuarios():
    response = bc.sendToBus("dbcon", {"instruccion": "getAllUsuarios"})
    return json.dumps(response)

def crearUsuario(token, nombre, precio, puntos_por_servicio):
    
        sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})
    
        if sesion["status"] == False:
            return json.dumps({"status": False, "data": "Token inválido"})
        elif sesion["data"]["role"] != "admin":
            return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
        
        response = bc.sendToBus("dbcon", 
            {"instruccion": "createUsuario", 
                "nombre": nombre, 
                "precio": precio,
                "puntos_por_servicio": puntos_por_servicio
            }
        )
    
        return json.dumps(response)

def editarUsuario(token, id, nombre, precio, puntos_por_servicio):
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})
    
    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
    
    response = bc.sendToBus("dbcon", {"instruccion": "updateUsuario", 
            "id": id,
            "nombre": nombre, 
            "precio": precio,
            "puntos_por_servicio": puntos_por_servicio
    })
    return json.dumps(response)

def eliminarUsuario(token, id):
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})
    
    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
    
    response = bc.sendToBus("dbcon", {"instruccion": "deleteUsuario", 
            "id": id
    })
    return json.dumps(response)