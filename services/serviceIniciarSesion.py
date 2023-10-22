import busConnect as bc
import json

def IniciarSesion(data):
    usuario = json.loads(data[5:])
    
    response = bc.sendToBus("dbcon", {
        "instruccion": "getUser",
        "email": usuario['email'],
        "password": usuario['password']
    })

    # En caso de éxito, generamos el token y retornamos la información.
    if response["status"] == "success":
        output = bc.sendToBus("svses", {
            "instruccion": "create_token",
            "email": usuario['email'],
            "nombre": response["data"]["nombre"],
            "role": response["data"]["nombre_rol"]
        })

        return json.dumps({
            "status": "success",
            "nombre": response["data"]["nombre"],
            "email": response["data"]["email"],
            "rol": response["data"]["nombre_rol"],
            "token": output["token"]
        })

    # En caso de error, retornamos el mensaje de error.
    return json.dumps({
        "status": "error",
        "error": response["data"]
    })
