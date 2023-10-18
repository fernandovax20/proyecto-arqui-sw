import bcrypt
import jwt
import datetime
import json

# Definir una llave secreta (es importante mantener esta llave segura)
SECRET_KEY = "thebestsoaservice2023"

def hash_password(password: str) -> str:
    # Hash a password using bcrypt with a salt (10 rounds)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10))
    return hashed_password.decode('utf-8')  # Convertir de bytes a str antes de retornar

def verify_password(password: str, hashed_password: str) -> bool:
    # Verificar una contraseña contra un hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(email, role):
    # Crear un token JWT
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # El token expira en 1 hora
    payload = {
        "email": email,
        "role": role,
        "exp": expiration  # Tiempo de expiración
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    # Verificar un token JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # El token es válido, retornar la información del payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


def intruccion(data=None):
    datos = json.loads(data[5:])
    print("entra",datos)
    if datos["instruccion"] == "hash_password":
        return hash_password(datos["password"])
    elif datos["instruccion"] == "verify_password":
        return verify_password(datos["password"], datos["hashed_password"])
    elif datos["instruccion"] == "create_token":
        return create_token(datos["email"], datos["role"])
    elif datos["instruccion"] == "verify_token":
        return verify_token(datos["token"])
print("no entro pero ejecuta por alguna razon")
# Uso:
# Encriptar una contraseña
password = "123"
hashed_password = hash_password(password)
print(f'Contraseña encriptada: {hashed_password}')

# Verificar una contraseña
is_valid = verify_password("123", "$2b$10$6CaxPcda7RtARiUtlo1xq.0KU3rdjkeLid2tNiDFWyGPP1WTHQMpO")
print(f'La contraseña es válida: {is_valid}')


# Crear un token
email = "usuario@example.com"
role = "admin"
token = create_token(email, role)
print(f'Token: {token}')

# Verificar un token
verification_result = verify_token(token)
print(f'Verificación: {verification_result}')