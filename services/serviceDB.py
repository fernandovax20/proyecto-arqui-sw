from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json
import bcrypt

# Conexión a la base de datos
engine = create_engine('postgresql+psycopg://barberhouse:soa123@localhost/barberhouse')

# Reflejar la estructura de la base de datos existente
metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

# Acceso a las clases mapeadas
Servicio = Base.classes.Servicios
Users = Base.classes.Users
Roles = Base.classes.Roles

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def instruccion(data=None):
    print(data, "desde dbcon", data[5:])
    datos = json.loads(data)

    instruct_map = {
        "getAllServicios": getAllServicios,
        "getUser": lambda: getUser(datos["email"], datos["password"]),
        "registrarUsuario": lambda: registrarUsuario(datos["nombre"], datos["email"], datos["password"])
    }
    
    func = instruct_map.get(datos["instruccion"])
    return func() if func else None

def getAllServicios():
    servicios = [
        {
            "id": servicio.id,
            "nombre": servicio.nombre,
            "description": servicio.description,
            "precio": servicio.precio,
            "puntos_por_servicio": servicio.puntos_por_servicio
        } for servicio in session.query(Servicio).all()
    ]

    return json.dumps({"servicios": servicios}, ensure_ascii=False, indent=2)

def getUser(email, password):
    usuario_db = (session.query(Users, Roles)
                  .join(Roles, Users.id_rol == Roles.id)
                  .filter(Users.email == email)
                  .first())

    if usuario_db and bcrypt.checkpw(password.encode('utf-8'), usuario_db.Users.password.encode('utf-8')):
        usuario, rol = usuario_db
        return json.dumps({
            "status": "success",
            "data": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "nombre_rol": rol.nombre_rol
            }
        })

    return json.dumps({"status": "error", "data": "Usuario o password incorrecto"})

def registrarUsuario(nombre, email, password):
    if session.query(Users).filter(Users.email == email).first():
        return json.dumps({"status": "error", "data": "Error al registrar usuario"})

    password_encriptado = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    nuevo_usuario = Users(nombre=nombre, email=email, password=password_encriptado, id_rol=2)

    session.add(nuevo_usuario)
    session.commit()

    return json.dumps({"status": "success", "data": "Usuario registrado exitosamente"})
