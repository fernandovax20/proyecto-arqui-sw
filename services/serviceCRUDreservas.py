import json
import busConnect as bc

def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data)
    
    func_map = {
        "ListarReservas": lambda: getAllReservas(datos["token"]),
        "ListarFechasReservas": lambda: getAllFechasReservas(datos["token"]),
        "createReserva": lambda: createReserva(datos["token"], datos["id_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
        "updateReserva": lambda: updateReserva(),
        "deleteReserva": lambda: deleteReserva(datos["id"]),
        "ConfirmarAsistencia": lambda: ConfirmarAsistencia(datos["id"]),
    }

    func = func_map.get(datos["instruccion"])
    return func() if func else json.dumps({"status": False, "data": "Instrucción no reconocida"})

def getAllReservas(token):
    
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
        
    response = bc.sendToBus("dbcon", {"instruccion": "getAllReservas"})
    return json.dumps(response, separators=(',', ':'))

def getAllFechasReservas(token):
        
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
        
    response = bc.sendToBus("dbcon", {"instruccion": "getAllFechasReservas"})
    return json.dumps(response, separators=(',', ':'))

def createReserva(token, id_usuario, id_servicio, fecha_hora_utc):

    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})

    response = bc.sendToBus("dbcon", {
        "instruccion": "createReserva", 
        "id_usuario": id_usuario, 
        "id_servicio": id_servicio, 
        "fecha_hora_utc": fecha_hora_utc
    })
    return json.dumps(response, separators=(',', ':'))

def updateReserva(id, nombre, email, telefono, fecha, hora, cantidad_personas, estado):
    print("Entra a updateReserva")

def deleteReserva(id):
    print("Entra a deleteReserva")

def ConfirmarAsistencia(id):
    print("Entra a ConfirmarAsistencia")