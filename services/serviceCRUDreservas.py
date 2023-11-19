import json
import busConnect as bc

def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data)
    
    func_map = {
        "ListarReservas": lambda: getAllReservas(datos["token"]),
        "ListarFechasReservas": lambda: getAllFechasReservas(),
        "reservasPorUserId": lambda: reservasPorUserId(datos["token"], datos["id_usuario"]),
        "createReserva": lambda: createReserva(datos["token"], datos["id_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
        "updateReserva": lambda: updateReserva(datos["token"], datos["id_reserva"], datos["id_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
        "deleteReserva": lambda: deleteReserva(datos["token"], datos["id_reserva"]),
        "ConfirmarAsistencia": lambda: ConfirmarAsistencia(datos["token"], datos["id_reserva"]),
        "reservasCliente": lambda: reservasCliente(datos["token"])
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

def getAllFechasReservas():

    response = bc.sendToBus("dbcon", {"instruccion": "getAllFechasReservas"})
    return json.dumps(response, separators=(',', ':'))

def reservasCliente(token):
        
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "cliente":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
        
    email = sesion["data"]["email"]
    response = bc.sendToBus("dbcon", {"instruccion": "reservasCliente", "email": email})
    return json.dumps(response, separators=(',', ':'))

def reservasPorUserId(token, id_usuario):
            
        sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})
    
        if sesion["status"] == False:
            return json.dumps({"status": False, "data": "Token inválido"})
        elif sesion["data"]["role"] != "admin":
            return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})
            
        response = bc.sendToBus("dbcon", {"instruccion": "reservasPorUserId", "id_usuario": id_usuario})
        return json.dumps(response, separators=(',', ':'))

def createReserva(token, id_usuario, id_servicio, fecha_hora_utc):

    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    response = ""

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] == "admin":
        response = bc.sendToBus("dbcon", {
            "instruccion": "createReserva", 
            "id_usuario": id_usuario, 
            "id_servicio": id_servicio, 
            "fecha_hora_utc": fecha_hora_utc
        })
    elif sesion["data"]["role"] == "cliente":
        email = sesion["data"]["email"]
        response = bc.sendToBus("dbcon", {
            "instruccion": "createClienteReserva", 
            "email_usuario": email, 
            "id_servicio": id_servicio, 
            "fecha_hora_utc": fecha_hora_utc
        })
    else:
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})

    
    return json.dumps(response, separators=(',', ':'))

def updateReserva(token, id_reserva, id_usuario, id_servicio, fecha_hora_utc):
    
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})

    response = bc.sendToBus("dbcon", {
        "instruccion": "updateReserva", 
        "id_reserva": id_reserva, 
        "id_usuario": id_usuario, 
        "id_servicio": id_servicio, 
        "fecha_hora_utc": fecha_hora_utc
    })
    return json.dumps(response, separators=(',', ':'))

def deleteReserva(token, id):
        
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})

    response = bc.sendToBus("dbcon", {
        "instruccion": "deleteReserva", 
        "id_reserva": id
    })
    return json.dumps(response, separators=(',', ':'))

def ConfirmarAsistencia(token, id):
            
    sesion = bc.sendToBus("svses", {"instruccion": "verify_token", "token": token})

    if sesion["status"] == False:
        return json.dumps({"status": False, "data": "Token inválido"})
    elif sesion["data"]["role"] != "admin":
        return json.dumps({"status": False, "data": "No tienes permisos para realizar esta acción"})

    response = bc.sendToBus("dbcon", {
        "instruccion": "ConfirmarAsistencia", 
        "id_reserva": id
    })
    return json.dumps(response, separators=(',', ':'))

def reservaCliente(token):
    print("reservaCliente")