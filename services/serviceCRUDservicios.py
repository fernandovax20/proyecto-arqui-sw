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
    response = bc.sendToBus("dbcon", {"instruccion": "getAllServicios"})
    return json.dumps(response)

def editarServicio(token, nombre, description, precio, duracion, puntos_por_servicio):
    response = bc.sendToBus("dbcon", {"instruccion": "getAllServicios"})
    return json.dumps(response)

def eliminarServicio(token, id):
    response = bc.sendToBus("dbcon", {"instruccion": "getAllServicios"})
    return json.dumps(response)