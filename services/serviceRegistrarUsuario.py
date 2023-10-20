
import busConnect as bc
import json

def RegistrarUsuario(data):
    usuario = json.loads(data[5:])
    nombre = usuario['nombre']
    email = usuario['email']
    password = usuario['password']

    print("Registrando usuario...")
    print("Nombre: ", nombre, "Email: ", email, "Password: ", password)

    response = bc.sendToBus("dbcon", {
       "instruccion": "registrarUsuario", 
       "nombre": nombre,
       "email": email, 
       "password": password
    })



    return json.dumps({"status": response["status"], "data": response["data"]})