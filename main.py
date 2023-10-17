import socket
import json

def send_list_request():
    """Función para enviar una solicitud de listar al servicio."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Conectar al servicio
        server_address = ('localhost', 5000)
        sock.connect(server_address)
        print(f'Conectado a {server_address[0]} puerto {server_address[1]}')

        # Crear y enviar el mensaje
        message = 'lista'.encode()
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

        print(service_name)        # Debería imprimir: lista
        print(status)              # Debería imprimir: OK
        print(data)                # Debería imprimir el diccionario con los nombres
        print(data["nombres"])     # Debería imprimir el diccionario con los nombres
        print(data["nombres"][0])  # Debería imprimir el diccionario con los nombres

        #print(f'Respuesta recibida: {response}')

if __name__ == "__main__":
    send_list_request()
