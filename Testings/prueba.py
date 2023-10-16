import socket

def send_initialization_to_bus():
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el socket al puerto donde el bus está escuchando
    server_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Construir y enviar el mensaje de inicialización
        message = b'00010sinitservi'
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Esperar y recibir la respuesta del bus
        header = sock.recv(5)
        if not header:
            print("No response received")
            return

        amount_expected = int(header)
        amount_received = 0
        response = ""

        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            if not chunk:
                break
            amount_received += len(chunk)
            response += chunk.decode()

        print(f"Received response: {response}")

    finally:
        print('closing socket')
        sock.close()

if __name__ == "__main__":
    send_initialization_to_bus()




