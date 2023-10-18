from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json

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

def instruccion(data=None):
    datos = json.loads(data[5:])

    if datos["instruccion"] == "getAllServicios":
        return getAllServicios()
