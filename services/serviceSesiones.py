import bcrypt
import jwt
import datetime
import json

# Definir una llave secreta (es importante mantener esta llave segura)
SECRET_KEY = "thebestsoaservice2023"

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

def instruccion(data=None):
    """Ejecuta una instrucción basada en el contenido de 'data'."""
    datos = json.loads(data[5:])
    
    func_map = {
        "create_token": lambda: create_token(datos["email"], datos["nombre"], datos["role"]),
        "verify_token": lambda: verify_token(datos["token"])
    }

    func = func_map.get(datos["instruccion"])
    return func() if func else json.dumps({"status": False, "data": "Instrucción no reconocida"})
