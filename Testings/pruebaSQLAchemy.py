from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

"""
Instalar estos paquetes:
pip install sqlalchemy
pip install psycopg2-binary
"""

# Conexión a la base de datos
engine = create_engine('postgresql://giadach:soa123@localhost/proyecto-arqui')

# Reflejar la estructura de la base de datos existente
metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

# Acceso a las clases mapeadas
Todo = Base.classes.todo
Task = Base.classes.task

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Leer datos
def list_data():
    for todo in session.query(Todo).all():
        print(f'Todo ID: {todo.id}, Nombre: {todo.nombre}')
        for task in todo.task_collection:
            print(f'  Task ID: {task.id}, Nombre: {task.name}, Completado: {task.completado}')

# Actualizar datos
def update_data(task_id, new_status):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completado = new_status
        session.commit()

# Eliminar datos
def delete_data(task_id):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        session.delete(task)
        session.commit()

# Ejemplo de uso
if __name__ == '__main__':
    list_data()
    #update_data(1, True)
    #list_data()
    #delete_data(1)
    #list_data()
