import bcrypt
import jwt
import datetime
import json

# Definir una llave secreta (es importante mantener esta llave segura)
SECRET_KEY = "thebestsoaservice2023"

def create_token(email, role):
    # Crear un token JWT
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # El token expira en 1 hora
    payload = {
        "email": email,
        "role": role,
        "exp": expiration  # Tiempo de expiración
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return json.dumps({"token":token})

def verify_token(token):
    # Verificar un token JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # El token es válido, retornar la información del payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def instruccion(data=None):
    datos = json.loads(data[5:])
    if datos["instruccion"] == "create_token":
        return create_token(datos["email"], datos["role"])
    elif datos["instruccion"] == "verify_token":
        return verify_token(datos["token"])

"""
# Uso:
# Encriptar una contraseña

# Crear un token
email = "usuario@example.com"
role = "admin"
token = create_token(email, role)
print(f'Token: {token}')

# Verificar un token
verification_result = verify_token(token)
print(f'Verificación: {verification_result}')

"""