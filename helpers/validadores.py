import re

def es_email_valido(email):
    """Verifica si un dato es un email válido."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def es_nombre_valido(nombre):
    """Verifica si un dato contiene solo letras y espacios."""
    return all(caracter.isalpha() or caracter.isspace() for caracter in nombre)