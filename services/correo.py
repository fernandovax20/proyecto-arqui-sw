from datetime import datetime, timedelta
import busConnect as bc

# Librerias para enviar correo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime, timedelta
import schedule
import time
import pytz 

def enviar_correo(destinatario_email, asunto, cuerpo):
    # Configura el servidor SMTP y el puerto (en este caso, para Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    remetente_email = 'barberhouse.mail@gmail.com'

    # Crea el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remetente_email
    mensaje['To'] = destinatario_email
    mensaje['Subject'] = asunto
    # remetente_password = 'barberhouse123'
    remetente_password = 'idpw atgf zvht caby'

    

    # Agrega el cuerpo del mensaje
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Inicia la conexión con el servidor SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Inicia sesión en el servidor
        server.starttls()
        server.login(remetente_email, remetente_password)

        # Envía el mensaje
        server.sendmail(remetente_email, destinatario_email, mensaje.as_string())

    print('Correo electrónico enviado exitosamente.')

# Invocando a la funcion del mail

destinatario = 'jcuitinomendoza@gmail.com'
asunto = 'Confirmacion de Hora'
cuerpo_mensaje = 'Confirma la hora panita'

# enviar_correo(destinatario, asunto, cuerpo_mensaje)

def enviar_recordatorio(nombre_usuario, id_reserva, destinatario_email, fecha_reserva):
    asunto = f'Recordatorio de Reserva para Usuario {nombre_usuario}'
    cuerpo = f'Hola,\n\nEste es un recordatorio para la reserva con ID {id_reserva}. La fecha de reserva es {fecha_reserva}.'
    cuerpo += '\nIngrese al siguiente link para confirmar su hora: http://localhost:5001/api?id_reserva=' + str(id_reserva)
    enviar_correo(destinatario_email, asunto, cuerpo)

def procesar_correos(correos_para_enviar):
    zona_horaria_chile = pytz.timezone('Chile/Continental')
    ahora = datetime.now(zona_horaria_chile)

    for correo_info in correos_para_enviar:
        try:
            id_reserva = correo_info['id']
            nombre_usuario = correo_info['nombre_usuario']
            destinatario_email = correo_info['email_usuario']
            fecha_reserva_str = correo_info['hora_local']
            correo_enviado = correo_info['correo_enviado']

            fecha_reserva = datetime.strptime(fecha_reserva_str, '%Y-%m-%d %H:%M')
            fecha_reserva = zona_horaria_chile.localize(fecha_reserva)

            # Calcula el tiempo hasta la reserva
            tiempo_hasta_reserva = (fecha_reserva - ahora).total_seconds()

            if 0 < tiempo_hasta_reserva <= 3600 and not correo_enviado:
                print(f"Enviando correo inmediatamente a {destinatario_email} para la reserva en {tiempo_hasta_reserva} segundos.")
                enviar_recordatorio(nombre_usuario, id_reserva, destinatario_email, fecha_reserva_str)
                marcar_correo_enviado(id_reserva)
            else:
                print(f"La hora de envío ya ha pasado o el correo ya ha sido enviado para {destinatario_email} con hora {fecha_reserva}.")

        except Exception as e:
            print(f"Error al procesar correo: {e}")

def enviar_formulario_feedback(id_reserva, nombre_usuario, destinatario_email):
    asunto = f'Feedback de Reserva para Usuario {nombre_usuario}'
    cuerpo = f'Hola,\n\nPor favor, ingrese al siguiente link para completar el formulario de feedback para la reserva con ID {id_reserva}.'
    cuerpo += '\nIngrese al siguiente link para completar el formulario de feedback: http://localhost:5001/mostrar-formulario/' + str(id_reserva)
    enviar_correo(destinatario_email, asunto, cuerpo)

def enviar_feedback_correo(correos_para_enviar):

    for correo_info in correos_para_enviar:
        try:
            id_reserva = correo_info['id']
            nombre_usuario = correo_info['nombre_usuario']
            destinatario_email = correo_info['email_usuario']
            estado = correo_info['estado']
            feedback_enviado = correo_info['feedback_enviado']

            if estado == 'atendido' and not feedback_enviado:
                print(f"Enviando correo inmediatamente a {destinatario_email} para la reserva {id_reserva}.")
                enviar_formulario_feedback( id_reserva, nombre_usuario, destinatario_email)
                marcar_feedback_enviado(id_reserva)
            else:
                print(f"La hora de envío ya ha pasado o el correo ya ha sido enviado para {destinatario_email}.")

        except Exception as e:
            print(f"Error al procesar correo: {e}")

def enviar_feedback():
    try:
        # Obtiene las confirmaciones de la base de datos
        response = bc.sendToBus("dbcon", {"instruccion": "feedbackFaltantes"})

        # Verifica si la respuesta contiene la clave 'reservas'
        if 'feedback_faltante' in response:
            # Procesa las reservas si existen
            return response['feedback_faltante']
        else:
            print("La respuesta no contiene feedback_faltante.")
            return []
    except Exception as e:
        print(f"Ocurrió un error al procesar las confirmaciones: {e}")

def marcar_feedback_enviado(id_reserva):
    try:
        # Marca el correo como enviado en la base de datos
        response = bc.sendToBus("dbcon", {"instruccion": "feedbackEnviado", "id_reserva": id_reserva})
        print("Response: ", response)
    except Exception as e:
        print(f"Ocurrió un error al marcar el correo como enviado: {e}")

def marcar_correo_enviado(id_reserva):
    try:
        # Marca el correo como enviado en la base de datos
        response = bc.sendToBus("dbcon", {"instruccion": "correoEnviado", "id_reserva": id_reserva})
        print("Response: ", response)
    except Exception as e:
        print(f"Ocurrió un error al marcar el correo como enviado: {e}")

def procesar_confirmaciones():
    try:
        # Obtiene las confirmaciones de la base de datos
        response = bc.sendToBus("dbcon", {"instruccion": "ConfirmaReserva"})

        # Verifica si la respuesta contiene la clave 'reservas'
        if 'reservas' in response:
            # Procesa las reservas si existen
            return response['reservas']
        else:
            print("La respuesta no contiene reservas.")
            return []
    except Exception as e:
        print(f"Ocurrió un error al procesar las confirmaciones: {e}")


# Ejecuta el cronjob
while True:
    confirmaciones = procesar_confirmaciones()
    lista_feedback = enviar_feedback()
    procesar_correos(confirmaciones)
    enviar_feedback_correo(lista_feedback)
    schedule.run_pending()
    time.sleep(30)






