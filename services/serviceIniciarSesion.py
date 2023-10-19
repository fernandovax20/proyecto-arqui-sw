import busConnect as bc
import json


Usuarios = {
    "usuarios": [
        {
            "email": "c@c.cl",
            "password": "123",
        }
    ]
}

enSesion = {
    "status": "NK",
}

def IniciarSesion(data):
    usuario = json.loads(data[5:])
    email = usuario['email']
    password = usuario['password']
    response = bc.sendToBus("dbcon", {
        "instruccion": "getUser", 
        "email": email, 
        "password": password
    })


    if(response["status"] == "success"):
        output = bc.sendToBus("svses", { "instruccion": "create_token", "email": email, "role": response["data"]["nombre_rol"] })
        print("El token generado es: ", output["token"])

        return json.dumps({"user":response, "token":output["token"]})

    for i in range(len(Usuarios["usuarios"])):
        if(Usuarios["usuarios"][i]["email"] == email):
            if(Usuarios["usuarios"][i]["password"] == password):
                enSesion["status"] = "OK"
                return json.dumps(enSesion)
            else:
                enSesion["status"] = "NK"
                return json.dumps(enSesion)
    enSesion["status"] = "NK"
    return json.dumps(enSesion)