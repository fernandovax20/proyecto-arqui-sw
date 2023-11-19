from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
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
Reserva = Base.classes.Reserva

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def instruccion(data=None):
    datos = json.loads(data)

    instruct_map = {
        "getAllServicios": getAllServicios,
        "createServicio": lambda: createServicio(datos["nombre"], datos["precio"], datos["puntos_por_servicio"]),
        "updateServicio": lambda: updateServicio(datos["id"], datos["nombre"], datos["precio"], datos["puntos_por_servicio"]),
        "deleteServicio": lambda: deleteServicio(datos["id"]),
        "getAllUsuarios": getAllUsuarios,
        "createUsuario": lambda: createUsuario(datos["nombre"], datos["email"], datos["password"], datos["nombre_rol"]),
        "updateUsuario": lambda: updateUsuario(datos["id"], datos["nombre"], datos["email"], datos["password"], datos["nombre_rol"]),
        "deleteUsuario": lambda: deleteUsuario(datos["id"]),
        "getUser": lambda: getUser(datos["email"], datos["password"]),
        "registrarUsuario": lambda: registrarUsuario(datos["nombre"], datos["email"], datos["password"]),
        "getAllReservas": getAllReservas,
        "getAllFechasReservas": getAllFechasReservas,
        "createReserva": lambda: createReserva(datos["id_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
    }
    
    func = instruct_map.get(datos["instruccion"])
    return func() if func else None

###########################################################################################################
# Funciones Servicios
def getAllServicios():
    servicios = [
        {
            "id": servicio.id,
            "nombre": servicio.nombre,
            "precio": servicio.precio,
            "puntos_por_servicio": servicio.puntos_por_servicio
        } for servicio in session.query(Servicio).all()
    ]
    return json.dumps({"servicios": servicios}, ensure_ascii=False, separators=(',', ':'))

def createServicio(nombre, precio, puntos_por_servicio):
    nuevo_servicio = Servicio(nombre=nombre, precio=precio, puntos_por_servicio=puntos_por_servicio)
    session.add(nuevo_servicio)
    session.commit()
    return json.dumps({"status": "success", "data": "Servicio creado exitosamente"}, separators=(',', ':'))

def updateServicio(id, nombre, precio, puntos_por_servicio):
    try:
        # Selecciona el servicio para actualizar y bloquea la fila
        servicio = session.query(Servicio).filter(Servicio.id == id).with_for_update().one_or_none()

        # Si el servicio no existe, retorna un mensaje de error
        if servicio is None:
            return json.dumps({"status": "error", "data": "Servicio no encontrado"}, separators=(',', ':'))

        # Actualiza los campos del servicio
        servicio.nombre = nombre
        servicio.precio = precio
        servicio.puntos_por_servicio = puntos_por_servicio

        # Confirma los cambios en la base de datos
        session.commit()
        return json.dumps({"status": "success", "data": "Servicio actualizado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        # En caso de error, deshace los cambios
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))


def deleteServicio(id):
    try:
        # Encuentra el servicio a eliminar
        servicio = session.query(Servicio).filter(Servicio.id == id).one_or_none()

        if servicio is None:
            return json.dumps({"status": "error", "data": "Servicio no encontrado"}, separators=(',', ':'))

        session.delete(servicio)
        session.commit()
        return json.dumps({"status": "success", "data": "Servicio eliminado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))


###########################################################################################################
# Funciones Usuarios
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

    return json.dumps({"status": "error", "data": "Usuario o password incorrecto"}, separators=(',', ':'))

def registrarUsuario(nombre, email, password):
    if session.query(Users).filter(Users.email == email).first():
        return json.dumps({"status": "error", "data": "Error al registrar usuario"}, separators=(',', ':'))

    password_encriptado = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    nuevo_usuario = Users(nombre=nombre, email=email, password=password_encriptado, id_rol=2)

    session.add(nuevo_usuario)
    session.commit()

    return json.dumps({"status": "success", "data": "Usuario registrado exitosamente"}, separators=(',', ':'))

def getAllUsuarios():
    usuarios = [
        {
            "id": usuario.Users.id,  # Cambiado de usuario.id a usuario.Users.id
            "nombre": usuario.Users.nombre,
            "email": usuario.Users.email,
            "nombre_rol": usuario.Roles.nombre_rol  # Asumiendo que quieres el nombre del rol
        } for usuario in session.query(Users, Roles).join(Roles, Users.id_rol == Roles.id).all()
    ]
    return json.dumps({"usuarios": usuarios}, ensure_ascii=False, separators=(',', ':'))

def createUsuario(nombre, email, password, rol):
    if session.query(Users).filter(Users.email == email).first():
        return json.dumps({"status": "error", "data": "Error al registrar usuario"}, separators=(',', ':'))

    password_encriptado = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    id_rol = session.query(Roles).filter(Roles.nombre_rol == rol).first().id
    nuevo_usuario = Users(nombre=nombre, email=email, password=password_encriptado, id_rol=id_rol)

    session.add(nuevo_usuario)
    session.commit()

    return json.dumps({"status": "success", "data": "Usuario registrado exitosamente"}, separators=(',', ':'))

def updateUsuario(id, nombre, email, password, rol):
    try:
        usuario = session.query(Users).filter(Users.id == id).with_for_update().one_or_none()

        if usuario is None:
            return json.dumps({"status": "error", "data": "Usuario no encontrado"}, separators=(',', ':'))

        usuario.nombre = nombre
        usuario.email = email
        usuario.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario.id_rol = session.query(Roles).filter(Roles.nombre_rol == rol).first().id

        session.commit()
        return json.dumps({"status": "success", "data": "Usuario actualizado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))
    
def deleteUsuario(id):
    try:
        usuario = session.query(Users).filter(Users.id == id).one_or_none()

        if usuario is None:
            return json.dumps({"status": "error", "data": "Usuario no encontrado"}, separators=(',', ':'))

        session.delete(usuario)
        session.commit()
        return json.dumps({"status": "success", "data": "Usuario eliminado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))

def getAllReservas():
    reservas = session.query(
        Reserva.id,
        Users.nombre.label("nombre_usuario"),
        Servicio.nombre.label("nombre_servicio"),
        func.to_char(func.timezone('Chile/Continental', Reserva.fecha_hora), 'YYYY-MM-DD HH24:MI').label('hora_local'),
        Reserva.estado
    ).join(
        Servicio, Reserva.id_servicio == Servicio.id
    ).join(
        Users, Reserva.id_usuario == Users.id
    ).filter(
        func.date(func.timezone('Chile/Continental', Reserva.fecha_hora)) == func.date(func.timezone('Chile/Continental', func.now()))
    ).all()

    resultado = [
        {
            "id": reserva.id,
            "nombre_usuario": reserva.nombre_usuario,
            "nombre_servicio": reserva.nombre_servicio,
            "hora_local": reserva.hora_local,
            "estado": reserva.estado
        } for reserva in reservas
    ]

    return json.dumps({"reservas": resultado}, ensure_ascii=False, separators=(',', ':'))

def getAllFechasReservas():
    # Obtener fecha y hora de cada reserva
    reservas_hoy = session.query(
        func.to_char(func.timezone('Chile/Continental', Reserva.fecha_hora), 'YYYY-MM-DD').label('fecha_local'),
        func.to_char(func.timezone('Chile/Continental', Reserva.fecha_hora), 'HH24:MI').label('hora_local')
    ).filter(
        func.date(func.timezone('Chile/Continental', Reserva.fecha_hora)) >= func.date(func.timezone('Chile/Continental', func.now()))
    ).all()

    # Agrupar horas por fecha
    fechas_reservas = defaultdict(list)
    for reserva in reservas_hoy:
        fecha = reserva.fecha_local[5:]  # Extraer MM-DD de la fecha
        hora = reserva.hora_local
        fechas_reservas[fecha].append(hora)

    # Convertir a formato deseado
    resultado = {fecha: horas for fecha, horas in fechas_reservas.items()}

    return json.dumps({"reservas": resultado}, ensure_ascii=False, separators=(',', ':'))

def createReserva(id_usuario, id_servicio, fecha_hora_utc):
    nueva_reserva = Reserva(id_usuario=id_usuario, id_servicio=id_servicio, fecha_hora=fecha_hora_utc)
    session.add(nueva_reserva)
    session.commit()
    return json.dumps({"status": "success", "data": "Reserva creada exitosamente"}, separators=(',', ':'))


