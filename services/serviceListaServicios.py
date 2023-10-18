import json
from helpers import busConnect as bc

def ListarServicios(data=None):
    response = bc.sendToBus("dbcon", {"instruccion": "getAllServicios", "data": "hola"})
    return json.dumps(response)