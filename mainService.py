import busConnect as bc
import json
import sys
import busConnect as bc

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
    #return "lista"+nombre_str



def main():
    if sys.argv[1] == "sumar":
        bc.GlobalServiceConnect("sumar", bc.process_data)
    elif sys.argv[1] == "lista":
        bc.GlobalServiceConnect("lista", listaDeNombres)
    else:
        print("Argumento no válido")

if __name__ == "__main__":
    main()
