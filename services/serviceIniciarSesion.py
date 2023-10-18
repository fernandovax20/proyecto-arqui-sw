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