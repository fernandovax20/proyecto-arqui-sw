import json
import socket

def sendToBus(nombreServicio, data=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Conectar al servicio
        server_address = ('localhost', 5000)
        sock.connect(server_address)
        print(f'Conectado a {server_address[0]} puerto {server_address[1]}')

        # Crear y enviar el mensaje
        message = nombreServicio.encode()
        print(f"{len(message):05d}".encode() + message)
        sock.sendall(f"{len(message):05d}".encode() + message)
        print('Solicitud enviada: lista')

        # Esperar la respuesta
        header = sock.recv(5).decode()
        response_length = int(header)
        response = sock.recv(response_length).decode()

        # Divide la respuesta en sus componentes
        service_name = response[:5]
        status = response[5:7]
        json_data = response[7:]

        # Convierte el string JSON en un diccionario de Python
        data = json.loads(json_data)
        tipo_de_dato = "servicios"
        #print(service_name)        # Debería imprimir: lista
        #print(status)              # Debería imprimir: OK
        #print(data)                # Debería imprimir el diccionario con los nombres
        print(data[tipo_de_dato])     # Debería imprimir el diccionario con los nombres
        #print(data["servicios"][0]) 

if __name__ == "__main__":
    salir = False
    while(not salir):
        print("""
        Bienvenido a Barber House\n
        1. Listar Servicios de Barbería\n
        2. Iniciar Sesión\n
        3. Registrarse\n
        4. Salir\n
        _________________________________________________________\n
              """)
        opcion = input("Ingrese opción: ")
        print("\n")

        if(opcion == "1"):
            print("Listar Servicios de Barbería")
            sendToBus("lsbar")
        elif(opcion == "2"):
            print("Iniciar Sesión")
        elif(opcion == "3"):
            print("Registrarse")
        elif(opcion == "4"):
            salir = True
            print("_________________________________________________________")