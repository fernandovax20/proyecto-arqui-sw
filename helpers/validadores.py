import re

import re

####################################################################################################################
# Validadores para usuarios
def obtener_email_valido():
    """Solicita y valida un email hasta que sea válido y no exceda los 50 caracteres."""
    while True:
        email = input("Ingrese su email: ")
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$"
        if re.match(pattern, email) and len(email) <= 50:
            return email
        else:
            print("Por favor, ingrese un email válido con un máximo de 50 caracteres.")

def obtener_nombre_valido():
    """Solicita y valida un nombre hasta que sea válido y no exceda los 50 caracteres."""
    while True:
        nombre = input("Ingrese su nombre: ")
        if all(caracter.isalpha() or caracter.isspace() for caracter in nombre) and len(nombre) <= 50:
            return nombre
        else:
            print("El nombre debe contener solo letras y espacios, y tener un máximo de 50 caracteres.")

####################################################################################################################
# Validadores para servicios
def validar_nombre_servicio():
    """Verifica si el nombre del servicio contiene solo letras y tiene una longitud máxima de 50 caracteres."""
    while True:
        nombre = input("Ingrese nombre del servicio: ")
        if re.match(r'^[A-Za-z\s]{1,50}$', nombre):
            return nombre
        else:
            print("El nombre debe contener solo letras, espacios y tener un máximo de 50 caracteres.")

def validar_precio_servicio():
    """Verifica si el precio del servicio es un número válido y no excede los 50.000."""
    while True:
        precio = input("Ingrese precio del servicio: ")
        if re.match(r'^\d+$', precio) and 0 < int(precio) <= 50000:
            return int(precio)
        else:
            print("El precio debe ser un número no mayor a 50.000.")


def validar_puntos_por_servicio():
    """Verifica si los puntos por servicio son un número válido y no exceden los 1.000."""
    while True:
        puntos = input("Ingrese puntos por servicio: ")
        if re.match(r'^\d+$', puntos) and 0 < int(puntos) <= 1000:
            return int(puntos)
        else:
            print("Los puntos por servicio deben ser un número no mayor a 1.000.")

def validar_id_servicio(ids_validos):
    """Verifica si el ID del servicio es un número positivo y está en la lista de IDs válidos."""
    while True:
        id_servicio = input("Ingrese id del servicio: ")
        if re.match(r'^\d+$', id_servicio):
            id_servicio = int(id_servicio)
            if id_servicio in ids_validos:
                return id_servicio
            else:
                print("El ID ingresado no es válido.")
        else:
            print("El ID debe ser un número positivo.")


