import busConnect as bc
import jwt
import datetime
import json

# Definir una llave secreta (es importante mantener esta llave segura)
SECRET_KEY = "thebestsoaservice2023"

def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data)
    
    func_map = {
        "create_token": lambda: create_token(datos["email"], datos["nombre"], datos["role"]),
        "verify_token": lambda: verify_token(datos["token"]),
        "IniciarSesion": lambda: IniciarSesion(datos["email"], datos["password"])
    }

    func = func_map.get(datos["instruccion"])
    return func() if func else json.dumps({"status": False, "data": "Instrucción no reconocida"})

def create_token(email, nombre, role):
    """Crea un token JWT."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
    payload = {
        "email": email,
        "nombre": nombre,
        "role": role,
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return json.dumps({"token": token})

def verify_token(token):
    """Verifica un token JWT."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return json.dumps({
            "status": True,
            "data": {
                "role": decoded["role"],
                "email": decoded["email"],
                "nombre": decoded["nombre"]
            }
        })
    except jwt.ExpiredSignatureError:
        return json.dumps({"status": False, "data": "Token expirado"})
    except jwt.InvalidTokenError:
        return json.dumps({"status": False, "data": "Token inválido"})

def IniciarSesion(email, password):
    
    response = bc.sendToBus("dbcon", {
        "instruccion": "getUser",
        "email": email,
        "password": password
    })

    # En caso de éxito, generamos el token y retornamos la información.
    if response["status"] == "success":
        output = create_token(email, response["data"]["nombre"], response["data"]["nombre_rol"])
        output = json.loads(output)

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
        "data": response["data"]
    })
