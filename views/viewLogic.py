from services import busConnect as bc
from prettytable import PrettyTable
import time
from .menuCliente import menuCliente 
from .menuAdmin import menuAdmin 
import pytz
from datetime import datetime, timedelta
from prettytable import PrettyTable

##############################################################################################
# Servicios
def ListarServicios():
    try:
        res = bc.sendToBus("servc", {"instruccion": "ListarServicios"})
        respuesta = res["servicios"]
        
        ids_servicios = []  

        tabla = PrettyTable()
        tabla.field_names = ["#", "Nombre", "Precio", "Puntos por Servicio"]
        for i, servicio in enumerate(respuesta, start=1):
            tabla.add_row([servicio["id"], servicio['nombre'], servicio['precio'], servicio['puntos_por_servicio']])
            ids_servicios.append(servicio["id"]) 
        print(tabla)
        time.sleep(2)
        return ids_servicios
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def CrearServicio(token,nombre, precio, puntos_por_servicio):
    try:
        res = bc.sendToBus("servc", 
            {"instruccion": "CrearServicio", 
                "token":token,
                "nombre": nombre, 
                "precio": precio, 
                "puntos_por_servicio": puntos_por_servicio})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def editarServicio(token, id, nombre, precio, puntos_por_servicio):
    try:
        res = bc.sendToBus("servc", 
            {"instruccion": "EditarServicio", 
                "token":token,
                "id": id,
                "nombre": nombre, 
                "precio": precio, 
                "puntos_por_servicio": puntos_por_servicio})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def eliminarServicio(token, id):
    try:
        res = bc.sendToBus("servc", 
            {"instruccion": "EliminarServicio", 
                "token":token,
                "id": id})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

##############################################################################################
# Sesiones
def IniciarSesion(email, password):
    try:
        res = bc.sendToBus("svses", 
            {"instruccion":"IniciarSesion",
                 "email": email, 
                 "password": password
        })
        if res["status"] == "success":
            if res["rol"] == "cliente":
                print("Bienvenido cliente")
                menuCliente(res["nombre"], res["rol"], res["token"])
            elif res["rol"] == "admin":
                print("Bienvenido administrador")
                menuAdmin(res["nombre"], res["rol"], res["token"])
        else:
            print("Error al iniciar sesión:", res["data"])
    except Exception:
        print(f"Ocurrió un error al iniciar sesion o en la sesion, porfavor intente mas tarde")
    

def RegistrarUsuario(nombre, email, password):
    try:
        res = bc.sendToBus("userc", 
                {"instruccion":"RegistrarUsuario",
                 "nombre": nombre, 
                 "email": email, 
                 "password": password
        })

        if res["status"] == "error":
            print("Error al registrar usuario:", res["data"])
        else:
            print(res["data"])
    except Exception :
        print(f"Ocurrió un error al registar el usuario, porfavor intente mas tarde")

##############################################################################################
#Usuarios

def ListarUsuarios(token):
    try:
        res = bc.sendToBus("userc", {"instruccion": "ListarUsuarios", "token":token})
        respuesta = res["usuarios"]

        tabla = PrettyTable()
        tabla.field_names = ["#", "Nombre", "Email", "Rol"]
        for i, usuario in enumerate(respuesta, start=1):
            tabla.add_row([usuario["id"], usuario['nombre'], usuario['email'], usuario['nombre_rol']])
        print(tabla)
        time.sleep(2)
        return respuesta
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def crearUsuario(token, nombre, email, password, role):
    try:
        res = bc.sendToBus("userc", 
            {"instruccion": "CrearUsuario", 
                "token":token,
                "nombre": nombre, 
                "email": email, 
                "password": password,
                "nombre_rol": role})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def editarUsuario(token, id, nombre, email, password, role):
    try:
        res = bc.sendToBus("userc", 
            {"instruccion": "EditarUsuario", 
                "token":token,
                "id": id,
                "nombre": nombre, 
                "email": email, 
                "password": password,
                "nombre_rol": role})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def eliminarUsuario(token, id):
    try:
        res = bc.sendToBus("userc", 
            {"instruccion": "EliminarUsuario", 
                "token":token,
                "id": id})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

##############################################################################################
#Reservas

def ListarReservas(token):
    try:
        res = bc.sendToBus("resec", {"instruccion": "ListarReservas", "token":token})
        respuesta = res["reservas"]

        tabla = PrettyTable()
        # Ajustando los nombres de las columnas según los datos
        tabla.field_names = ["ID", "Fecha y Hora", "Cliente", "Servicio", "Estado"]

        for reserva in respuesta:
            # Asegurándote de que los datos coincidan con los nombres de las columnas
            tabla.add_row([
                reserva["id"],
                reserva["hora_local"],
                reserva["nombre_usuario"],
                reserva["nombre_servicio"],
                reserva["estado"]
            ])
        print(tabla)
        time.sleep(2)
        return respuesta
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")


def ListarFechasReservas(token):
    try:
        res = bc.sendToBus("resec", {"instruccion": "ListarFechasReservas", "token":token})
        respuesta = res["reservas"]
        return respuesta
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def reservasPorUserId(token, id_usuario, retorno = True):
    try:
        res = bc.sendToBus("resec", {"instruccion": "reservasPorUserId", "token":token, "id_usuario": id_usuario})
        respuesta = res["reservas"]
        #print(respuesta)

        tabla = PrettyTable()

        tabla.field_names = ["ID", "Nombre_usuario", "Servicio", "Fecha_Hora", "Estado"]

        for reserva in respuesta:
            tabla.add_row([
                reserva["id"],
                reserva["nombre_usuario"],
                reserva["nombre_servicio"],
                reserva["hora_local"],
                reserva["estado"]
            ])
        if tabla.rowcount == 0:
            print("No hay reservas para este usuario")
        else:
            print(tabla)
        time.sleep(2)

        if retorno:
            id_reserva = 0

            while True:
                id_reserva = input("Ingrese el id de la reserva que desea editar: ")

                if id_reserva.isdigit():
                    id_reserva = int(id_reserva)  # Convertir a entero
                    if id_reserva in [reserva["id"] for reserva in respuesta]:
                        break
                    else:
                        print("Id no válido.")
                else:
                    print("Por favor, ingrese un número válido para el ID.")

            return id_reserva
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def crearReserva(token, id_usuario, id_servicio, fecha_hora_utc):
    try:
        res = bc.sendToBus("resec", 
            {"instruccion": "createReserva", 
                "token":token,
                "id_usuario": id_usuario, 
                "id_servicio": id_servicio, 
                "fecha_hora_utc": fecha_hora_utc})
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def updateReserva(token, id_reserva, id_usuario, id_servicio, fecha_hora_utc):
    try:
        res = bc.sendToBus("resec", 
            {"instruccion": "updateReserva", 
                "token":token,
                "id_reserva": id_reserva, 
                "id_usuario": id_usuario, 
                "id_servicio": id_servicio, 
                "fecha_hora_utc": fecha_hora_utc
            })
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def deleteReserva(token, id_reserva):
    try:
        res = bc.sendToBus("resec", 
            {"instruccion": "deleteReserva", 
                "token":token,
                "id_reserva": id_reserva
            })
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def ConfirmarAsistencia(token, id_reserva):
    try:
        res = bc.sendToBus("resec", 
            {"instruccion": "ConfirmarAsistencia", 
                "token":token,
                "id_reserva": id_reserva
            })
        return res
    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")


##############################################################################################
#Puntos y resrvas de Clientes

def ReservarHora(token, id_servicio, fecha_hora_utc):
    try:
        res = bc.sendToBus("resec", 
            {"instruccion": "createReserva", 
                "token":token,
                "id_usuario": 0,
                "id_servicio": id_servicio, 
                "fecha_hora_utc": fecha_hora_utc})
        return res

    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def MisReservas(token):
    try:
        res = bc.sendToBus("resec", 
            {"instruccion": "reservasCliente", 
                "token":token
            })
        respuesta = res["reservas"]

        tabla = PrettyTable()

        tabla.field_names = ["ID", "Nombre_usuario", "Servicio", "Fecha_Hora", "Estado"]

        for reserva in respuesta:
            tabla.add_row([
                reserva["id"],
                reserva["nombre_usuario"],
                reserva["nombre_servicio"],
                reserva["hora_local"],
                reserva["estado"]
            ])
        if tabla.rowcount == 0:
            print("No hay reservas para este usuario")
        else:
            print(tabla)
        time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

def MisPuntos(token):
    try:
        # Asumiendo que 'bc.sendToBus' devuelve una respuesta con los puntos del usuario
        res = bc.sendToBus("userc", 
            {"instruccion": "puntosCliente", 
                "token": token
            })

        # Verificar si la respuesta contiene el estado de éxito y extraer los puntos
        if res.get("status") == "success":
            puntos = res.get("data", {}).get("puntos", 0)
        else:
            print(f"Error: {res.get('data')}")
            return

        tabla = PrettyTable()
        tabla.field_names = ["Puntos"]

        # Agregar los puntos a la tabla
        tabla.add_row([puntos])

        # Imprimir la tabla
        if tabla.rowcount == 0:
            print("No hay puntos para este usuario")
        else:
            print(tabla)
        time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error: {e}, porfavor intente mas tarde")

##############################################################################################
#Calendarios
def mostrar_calendario():
    
    reservas = bc.sendToBus("resec", {"instruccion": "ListarFechasReservas"})
    reserved_hours = reservas["reservas"]

    timezone = 'Chile/Continental'
    start_hour_morning = 10
    end_hour_morning = 12
    start_hour_afternoon = 15
    end_hour_evening = 19

    # Reservas existentes
    

    two_week_days, two_week_schedule = generate_schedule_from_today(timezone, start_hour_morning, end_hour_morning, start_hour_afternoon, end_hour_evening, reserved_hours)
    calendar_display = create_calendar_table(two_week_days)
    print(calendar_display)

    selected_day = ""

    while True:
        selected_day = input("Ingrese la fecha que desea reservar (MM-DD): ")

        if selected_day in two_week_schedule:
            print(f"Horarios disponibles para el día {selected_day}:")
            horas = ""
            for hour in two_week_schedule[selected_day]:
                horas += hour + ", "
            print("\n")
            print(horas[:-2])
            print("\n")
            break;
        else:
            print("Fecha no disponible o fuera de rango.")

    selected_hour = ""
    while True:
        selected_hour = input("Ingrese la hora que desea reservar (HH:MM): ")

        if selected_hour in two_week_schedule[selected_day]:
            break;
        else:
            print("Hora no disponible o fuera de rango.")

    print(f"Fecha y hora seleccionada: {selected_day} {selected_hour}")
    fecha_hora_utc = convertir_a_utc(selected_day, selected_hour, timezone)
    #print(f"Fecha y hora seleccionada en UTC: {fecha_hora_utc}")
    return fecha_hora_utc

def generate_schedule_from_today(timezone, start_hour_morning, end_hour_morning, start_hour_afternoon, end_hour_evening, reserved_hours):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)

    # Inicia la programación desde el día actual, incluso si es domingo
    start_date = now if now.hour < end_hour_evening else now + timedelta(days=1)

    end_date = start_date + timedelta(days=14)  # Programación para dos semanas

    days = []
    schedule = {}
    while start_date < end_date:
        formatted_day = start_date.strftime("%m-%d")  # Formato mes-día
        day_hours = [f"{hour}:00" for hour in range(start_hour_morning, end_hour_morning + 1)] + \
                    [f"{hour}:00" for hour in range(start_hour_afternoon, end_hour_evening + 1)]
        # Filtrar horas reservadas
        day_hours = [hour for hour in day_hours if hour not in reserved_hours.get(formatted_day, [])]
        days.append((formatted_day, start_date.weekday(), len(day_hours)))
        schedule[formatted_day] = day_hours

        start_date += timedelta(days=1)

    return days, schedule


def create_calendar_table(days):
    calendar_table = PrettyTable()
    # Agregar columna para el domingo
    calendar_table.field_names = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    week = [''] * 7  # Ajustar para siete días
    for day, weekday, available_hours in days:
        week[weekday] = f"{day} ({available_hours}h)"
        if weekday == 6:  # Ahora el índice 6 representa el domingo
            calendar_table.add_row(week)
            week = [''] * 7

    # Si quedan días sin agregar al final de la lista
    if week != [''] * 7:
        calendar_table.add_row(week)

    return calendar_table

def convertir_a_utc(fecha_local, hora_local, timezone):
    tz = pytz.timezone(timezone)
    año_actual = datetime.now().year
    fecha_hora_local = datetime.strptime(f"{año_actual}-{fecha_local} {hora_local}", "%Y-%m-%d %H:%M")
    fecha_hora_local = tz.localize(fecha_hora_local)
    fecha_hora_utc = fecha_hora_local.astimezone(pytz.utc)
    return fecha_hora_utc.strftime("%Y-%m-%d %H:%M:%S UTC")