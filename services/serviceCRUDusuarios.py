import json
import busConnect as bc


def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data)
    
    func_map = {
        "ListarUsuarios": lambda: ListarUsuarios(datos["token"]),
        "CrearUsuario": lambda: crearUsuario(datos["token"], datos["nombre"], datos["email"], datos["password"], datos["nombre_rol"]),
        "EditarUsuario": lambda: editarUsuario(datos["token"],datos['id'], datos["nombre"], datos["email"], datos["password"], datos["nombre_rol"]),
        "EliminarUsuario": lambda: eliminarUsuario(datos["token"], datos['id']),
        "RegistrarUsuario": lambda: RegistrarUsuario(datos["nombre"], datos["email"], datos["password"])
    }

    func = func_map.get(datos["instruccion"])
    return func() if func else json.dumps({"status": False, "data": "Instrucción no reconocida"})

def ListarUsuarios(token):
    print("Entra a ListarUsuarios")
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})
    
    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
        
    response = bc.sendToBus("dbcon", {"instruccion": "getAllUsuarios"})
    return json.dumps(response)

def crearUsuario(token, nombre, email, password, role):
    
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
    
    response = bc.sendToBus("dbcon", 
        {"instruccion": "createUsuario", 
            "nombre": nombre, 
            "email": email,
            "password": password,
            "nombre_rol": role
        }
    )

    return json.dumps(response)

def editarUsuario(token, id, nombre, email, password, role):
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})
    
    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
    
    response = bc.sendToBus("dbcon", {"instruccion": "updateUsuario", 
            "id": id,
            "nombre": nombre, 
            "email": email,
            "password": password,
            "nombre_rol": role
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

def RegistrarUsuario(nombre, email, password):

    response = bc.sendToBus("dbcon", {
       "instruccion": "registrarUsuario", 
       "nombre": nombre,
       "email": email, 
       "password": password
    })

    return json.dumps({"status": response["status"], "data": response["data"]})