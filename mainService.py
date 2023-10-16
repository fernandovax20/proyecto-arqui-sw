import busConnect as bc

def listaDeNombres():
    nombre = ["benja", "jose", "juan", "pedro", "maria", "josefa", 
          "benjamin", "josefina", "josefino", "josefin"]
    nombre_str = ", ".join(nombre)
    print(nombre_str)
    return nombre_str


if __name__ == "__main__":

    #bc.GlobalServiceConnect("sumar", bc.process_data)
    bc.GlobalServiceConnect("lista", listaDeNombres)
