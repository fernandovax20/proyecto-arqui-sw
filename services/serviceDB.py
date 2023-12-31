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
Puntos_Acumulados = Base.classes.Puntos_Acumulados
FeedBack = Base.classes.Feedback

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
        "reservasPorUserId": lambda: reservas_by_user_id(datos["id_usuario"]),
        "createReserva": lambda: createReserva(datos["id_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
        "createClienteReserva": lambda: createClienteReserva(datos["email_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
        "updateReserva": lambda: updateReserva(datos["id_reserva"], datos["id_usuario"], datos["id_servicio"], datos["fecha_hora_utc"]),
        "deleteReserva": lambda: deleteReserva(datos["id_reserva"]),
        "ConfirmarAsistencia": lambda: ConfirmarAsistencia(datos["id_reserva"]),
        "reservasCliente": lambda: MisReservas(datos["email"]),
        "getPuntos": lambda: getPuntosByEmail(datos["email"]),
        "ConfirmaReserva": lambda: obtener_reservas_para_hoy(),
        "correoEnviado": lambda: correo_enviado(datos["id_reserva"]),
        "procesarConfirmacionesReserva": lambda: procesar_confirmaciones_Reserva(datos["id_reserva"]),
        "feedbackFaltantes": lambda: feedback_faltantes(),
        "feedbackEnviado": lambda: marcar_feedback_enviado(datos["id_reserva"]),
        "guardarFeedback": lambda: enviar_feedback(datos["id_reserva"], datos["valoracion"], datos["comentarios"])
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
        if password:
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

###########################################################################################################
# Funciones Reservas
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

def reservas_by_user_id(user_id):
    reservas = session.query(
        Reserva.id,
        Users.nombre.label('nombre_usuario'),
        Servicio.nombre.label('nombre_servicio'),
        func.to_char(func.timezone('Chile/Continental', Reserva.fecha_hora), 'YYYY-MM-DD HH24:MI').label('hora_local'),
        Reserva.estado,
        Reserva.correo_enviado,
        Reserva.confirmacion_presencial
    ).join(
        Servicio, Reserva.id_servicio == Servicio.id
    ).join(
        Users, Reserva.id_usuario == Users.id
    ).filter(
        Reserva.id_usuario == user_id
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

def createReserva(id_usuario, id_servicio, fecha_hora_utc):
    nueva_reserva = Reserva(id_usuario=id_usuario, id_servicio=id_servicio, fecha_hora=fecha_hora_utc)
    session.add(nueva_reserva)
    session.commit()
    return json.dumps({"status": "success", "data": "Reserva creada exitosamente"}, separators=(',', ':'))

def createClienteReserva(email_usuario, id_servicio, fecha_hora_utc):
    usuario = session.query(Users).filter(Users.email == email_usuario).one_or_none()

    if usuario is None:
        return json.dumps({"status": "error", "data": "Usuario no encontrado"}, separators=(',', ':'))
    
    nueva_reserva = Reserva(id_usuario=usuario.id, id_servicio=id_servicio, fecha_hora=fecha_hora_utc)
    session.add(nueva_reserva)
    session.commit()
    return json.dumps({"status": "success", "data": "Reserva creada exitosamente"}, separators=(',', ':'))

def updateReserva(id, id_usuario, id_servicio, fecha_hora_utc):
    try:
        reserva = session.query(Reserva).filter(Reserva.id == id).with_for_update().one_or_none()

        if reserva is None:
            return json.dumps({"status": "error", "data": "Reserva no encontrada"}, separators=(',', ':'))

        # Actualizar campos de la reserva existente
        reserva.id_usuario = id_usuario
        reserva.id_servicio = id_servicio
        reserva.fecha_hora = fecha_hora_utc

        session.commit()
        return json.dumps({"status": "success", "data": "Reserva actualizada exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))

def deleteReserva(id):
    try:
        reserva = session.query(Reserva).filter(Reserva.id == id).one_or_none()

        if reserva is None:
            return json.dumps({"status": "error", "data": "Reserva no encontrada"}, separators=(',', ':'))

        session.delete(reserva)
        session.commit()
        return json.dumps({"status": "success", "data": "Reserva eliminada exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))

def ConfirmarAsistencia(id_reserva):
    try:
        # Obtener la reserva y los puntos del servicio asociado
        reserva = session.query(Reserva, Servicio.puntos_por_servicio).join(
            Servicio, Reserva.id_servicio == Servicio.id
        ).filter(
            Reserva.id == id_reserva
        ).with_for_update().one_or_none()

        if reserva is None:
            return json.dumps({"status": "error", "data": "Reserva no encontrada"}, separators=(',', ':'))

        puntos_servicio = reserva.puntos_por_servicio

        # Actualizar la confirmación presencial de la reserva
        reserva.Reserva.confirmacion_presencial = True
        reserva.Reserva.estado = "atendido"  # Cambiar el estado de la reserva a 'asistio'

        # Buscar los puntos acumulados del usuario
        puntos_acumulados = session.query(Puntos_Acumulados).filter(
            Puntos_Acumulados.id_usuario == reserva.Reserva.id_usuario
        ).with_for_update().one_or_none()

        # Sumar los puntos del servicio a los puntos acumulados del usuario
        if puntos_acumulados:
            puntos_acumulados.puntos_acumulados += puntos_servicio
        else:
            # Crear un nuevo registro si no existe
            puntos_acumulados = Puntos_Acumulados(
                id_usuario=reserva.Reserva.id_usuario, 
                puntos_acumulados=puntos_servicio
            )
            session.add(puntos_acumulados)

        session.commit()
        return json.dumps({"status": "success", "data": "Reserva confirmada y puntos actualizados exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))

def MisReservas(email):
    usuario = session.query(Users).filter(Users.email == email).one_or_none()

    if usuario is None:
        return json.dumps({"status": "error", "data": "Usuario no encontrado"}, separators=(',', ':'))

    reservas = session.query(
        Reserva.id,
        Users.nombre.label('nombre_usuario'),
        Servicio.nombre.label('nombre_servicio'),
        func.to_char(func.timezone('Chile/Continental', Reserva.fecha_hora), 'YYYY-MM-DD HH24:MI').label('hora_local'),
        Reserva.estado,
        Reserva.correo_enviado,
        Reserva.confirmacion_presencial
    ).join(
        Servicio, Reserva.id_servicio == Servicio.id
    ).join(
        Users, Reserva.id_usuario == Users.id
    ).filter(
        Reserva.id_usuario == usuario.id
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

def getPuntosByEmail(email):
    usuario = session.query(Users).filter(Users.email == email).one_or_none()

    if usuario is None:
        return json.dumps({"status": "error", "data": "Usuario no encontrado"}, separators=(',', ':'))

    puntos_acumulados = session.query(Puntos_Acumulados).filter(
        Puntos_Acumulados.id_usuario == usuario.id
    ).one_or_none()

    puntos = puntos_acumulados.puntos_acumulados if puntos_acumulados else 0

    return json.dumps({"status": "success", "data": {"puntos": puntos}}, ensure_ascii=False, separators=(',', ':'))

def obtener_reservas_para_hoy():
    reservas_hoy = session.query(
        Reserva.id,
        Users.nombre.label('nombre_usuario'),
        Users.email,
        func.to_char(func.timezone('Chile/Continental', Reserva.fecha_hora), 'YYYY-MM-DD HH24:MI').label('hora_local'),
        Reserva.correo_enviado
    ).join(
        Servicio, Reserva.id_servicio == Servicio.id
    ).join(
        Users, Reserva.id_usuario == Users.id
    ).filter(
        func.date(func.timezone('Chile/Continental', Reserva.fecha_hora)) == func.date(func.timezone('Chile/Continental', func.now())),
        Reserva.correo_enviado == False
    ).all()

    resultado = [
        {
            "id": reserva.id,
            "nombre_usuario": reserva.nombre_usuario,
            "email_usuario": reserva.email,
            "hora_local": reserva.hora_local,
            "correo_enviado": reserva.correo_enviado
        } for reserva in reservas_hoy
    ]

    return json.dumps({"reservas": resultado}, ensure_ascii=False, separators=(',', ':'))

def correo_enviado(id_reserva):
    try:
        reserva = session.query(Reserva).filter(Reserva.id == id_reserva).with_for_update().one_or_none()

        if reserva is None:
            return json.dumps({"status": "error", "data": "Reserva no encontrada"}, separators=(',', ':'))

        reserva.correo_enviado = True

        session.commit()
        return json.dumps({"status": "success", "data": "Correo enviado actualizado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))

def procesar_confirmaciones_Reserva(id):
    try:
        reserva = session.query(Reserva).filter(Reserva.id == id).with_for_update().one_or_none()

        if reserva is None:
            return json.dumps({"status": "error", "data": "Reserva no encontrada"}, separators=(',', ':'))

        # Actualizar campos de la reserva existente
        reserva.estado = 'confirmado'

        session.commit()
        return json.dumps({"status": "success", "data": "Reserva confirmada exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))
    
def feedback_faltantes():
    feedback_faltantes = session.query(
        Reserva.id,
        Users.nombre.label('nombre_usuario'),
        Users.email,
        Reserva.estado,
        Reserva.feedback_enviado
    ).join(
        Servicio, Reserva.id_servicio == Servicio.id  # Asegúrate de que el modelo se llama 'Servicios'
    ).join(
        Users, Reserva.id_usuario == Users.id
    ).filter(
        Reserva.feedback_enviado == False,
        Reserva.estado == 'atendido'  
    ).all()

    resultado = [
        {
            "id": reserva.id,
            "nombre_usuario": reserva.nombre_usuario,
            "email_usuario": reserva.email,
            "estado": reserva.estado,
            "feedback_enviado": reserva.feedback_enviado
        } for reserva in feedback_faltantes
    ]

    return json.dumps({"feedback_faltante": resultado}, ensure_ascii=False, separators=(',', ':'))

def marcar_feedback_enviado(id):
    try:
        reserva = session.query(Reserva).filter(Reserva.id == id).with_for_update().one_or_none()

        if reserva is None:
            return json.dumps({"status": "error", "data": "Reserva no encontrada"}, separators=(',', ':'))

        # Actualizar campos de la reserva existente
        reserva.feedback_enviado = True

        session.commit()
        return json.dumps({"status": "success", "data": "Feedback enviado actualizado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))

def enviar_feedback(id_reserva, valoracion, comentarios):
    try:
        feedback = FeedBack(id_reserva=id_reserva, valoracion=valoracion, comentarios=comentarios)
        session.add(feedback)

        session.commit()
        return json.dumps({"status": "success", "data": "Feedback enviado actualizado exitosamente"}, separators=(',', ':'))
    except Exception as e:
        session.rollback()
        return json.dumps({"status": "error", "data": str(e)}, separators=(',', ':'))
