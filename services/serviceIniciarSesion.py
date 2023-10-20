import busConnect as bc
import json

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

        return json.dumps({"status": response["status"], "nombre": response["data"]["nombre"], "email": response["data"]["email"], "rol": response["data"]["nombre_rol"], "token": output["token"]})
    elif (response["status"] == "error"):
        return json.dumps({"status": response["status"], "error":response["data"]})

