import socket
import json
    
def GlobalServiceConnect(nombre, funcion):
    if len(nombre) != 5:
        return "El nombre debe tener 5 caracteres justos"
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5000)
    print(f'connecting to {server_address[0]} port {server_address[1]}')
    sock.connect(server_address)

    try:
        # Send initial data
        message = b'00011sinit' + nombre.encode('utf-8')
        print(f'sending {message!r}')
        sock.sendall(message)
        _receive_data(sock)  # Receive initial confirmation

        while True:
            print("Waiting for transaction")
            data = _receive_data(sock)
            
            print("Processing ...")
            ndata = funcion(data[5:])
            
            resp = '{:05d}'.format(len(ndata) + 5) + nombre + ndata
            print(f"Send answer (if needed): {resp}")
            sock.sendall(bytes(resp, 'utf-8'))

    finally:
        print('closing socket')
        sock.close()

def _receive_data(sock):
    """Helper function to receive data from socket."""
    amount_received = 0
    amount_expected = int(sock.recv(5))
    
    parts = []
    while amount_received < amount_expected:
        chunk = sock.recv(amount_expected - amount_received)
        amount_received += len(chunk)
        parts.append(chunk.decode())
        print(f'received {chunk!r}')

    return ''.join(parts)


def sendToBus(nombreServicio, data=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Conectar al servicio
        server_address = ('localhost', 5000)
        sock.connect(server_address)
        
        # Si hay data, conviértela a string y añádela al nombre del servicio
        message = nombreServicio
        if data:
            data_string = json.dumps(data)
            message += data_string
        message = message.encode()
        
        # Enviar el mensaje con su longitud al principio
        sock.sendall(f"{len(message):05d}".encode() + message)

        # Esperar la respuesta
        header = sock.recv(5).decode()
        response_length = int(header)
        response = sock.recv(response_length).decode()

        # Divide la respuesta en sus componentes
        # Nota: Las variables service_name y status se crearon pero no se usaron en tu código original
        service_name = response[:5]     # sumar, lista, etc.
        status = response[5:7]          # OK o NK
        json_data = response[7:]

        # Convierte el string JSON en un diccionario de Python y devuelve
        return json.loads(json_data)