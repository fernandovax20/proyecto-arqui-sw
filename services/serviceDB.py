from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json
import bcrypt

# Conexión a la base de datos
engine = create_engine('postgresql://barberhouse:soa123@localhost/barberhouse')

# Reflejar la estructura de la base de datos existente
metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

# Acceso a las clases mapeadas
Servicio = Base.classes.Servicios  # Asumiendo que la tabla se llama 'Servicios'

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()



def instruccion(data=None):
    datos = json.loads(data[5:])

    if datos["instruccion"] == "getAllServicios":
        return getAllServicios()
    elif datos["instruccion"] == "getUser":
        return getUser(datos["email"], datos["password"])
    


# Obtener Lista de Servicios
def getAllServicios():
    servicios = []
    for servicio in session.query(Servicio).all():
        servicio_dict = {
            "id": servicio.id,
            "nombre": servicio.nombre,
            "description": servicio.description,
            "precio": servicio.precio,
            "puntos_por_servicio": servicio.puntos_por_servicio
        }
        servicios.append(servicio_dict)
    servicios_json_obj = {"servicios": servicios}
    # Convertir el objeto JSON a una cadena JSON en formato UTF-8
    servicios_json_str = json.dumps(servicios_json_obj, ensure_ascii=False, indent=2)
    return servicios_json_str

# Verificar Usuario
def getUser(email, password):
    # Inicializar respuesta
    respuesta = {
        "status": None,
        "data": None
    }
    # Acceder a las tablas Users y Roles
    Users = Base.classes.Users
    Roles = Base.classes.Roles

    # Buscar el usuario por correo electrónico y hacer JOIN con la tabla Roles
    usuario_db = (session.query(Users, Roles)
                          .join(Roles, Users.id_rol == Roles.id)
                          .filter(Users.email == email)
                          .first())
    if usuario_db:
        usuario, rol = usuario_db  # Desempacar el resultado en las variables usuario y rol
        
        # Verificar la contraseña (asumiendo que la contraseña en la DB está encriptada con bcrypt)
        if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
            usuario_dict = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "nombre_rol": rol.nombre_rol  # Obtener el nombre del rol desde el objeto rol
            }
            respuesta["status"] = "success"
            respuesta["data"] = usuario_dict
        else:
            respuesta["status"] = "error"
            respuesta["data"] = "Usuario o password incorrecto"
    else:
        respuesta["status"] = "error"
        respuesta["data"] = "Usuario no encontrado"
    
    return json.dumps(respuesta)  # Convertir el diccionario respuesta a una cadena JSON
