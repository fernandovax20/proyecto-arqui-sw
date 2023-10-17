import busConnect as bc
import json

def listaDeNombres(data=None):  # Modificación aquí
    nombre = ["benja", "jose", "juan", "pedro", "maria", "josefa", 
          "benjamin", "josefina", "josefino", "josefin"]
    #nombre_str = ", ".join(nombre)
    #print(nombre_str)
    data = {
    "nombres": nombre
    }
    json_string = json.dumps(data)
    respuesta = "lista" + json_string
    return respuesta
    #return "lista"+nombre_str



if __name__ == "__main__":

    #bc.GlobalServiceConnect("sumar", bc.process_data)
    bc.GlobalServiceConnect("lista", listaDeNombres)
