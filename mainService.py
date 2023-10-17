import busConnect as bc
import json
import sys
import busConnect as bc
import serviceListaServicios as ls

def listaDeNombres(data=None):  # Modificación aquí
    nombre = ["benja", "jose", "juan", "pedro", "maria", "josefa", 
          "benjamin", "josefina", "josefino", "josefin"]
    #nombre_str = ", ".join(nombre)
    #print(nombre_str)
    data = {
    "nombres": nombre
    }
    json_string = json.dumps(data)
    respuesta = json_string
    return respuesta
def process_data(data):
    """
    Procesa la entrada del cliente. La entrada esperada es "sumar num1 num2".
    Devuelve una respuesta con la suma de num1 y num2.
    """
    
    parts = data.split()
    
    if len(parts) != 3 or parts[0] != "sumar":
        return "00012sumaNKError en formato"
    
    try:
        num1 = int(parts[1])
        num2 = int(parts[2])
        result = num1 + num2
        return "sumar"+str(result)
    except ValueError:
        return "00018sumaNKError en números"


def main():
    if sys.argv[1] == "sumar":
        bc.GlobalServiceConnect("sumar", process_data)

    elif sys.argv[1] == "lista":
        bc.GlobalServiceConnect("lista", listaDeNombres)

    elif sys.argv[1] == "lsbar": # este lanza la lista de los servicios de barberia
        bc.GlobalServiceConnect("lsbar", ls.ListarServicios)
    else:
        print("Argumento no válido")

if __name__ == "__main__":
    main()
