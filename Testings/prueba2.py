import socket

def send_sum_request(num1, num2):
    """Función para enviar una solicitud de suma al servicio."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Conectar al servicio
        server_address = ('localhost', 5000)
        sock.connect(server_address)
        print(f'Conectado a {server_address[0]} puerto {server_address[1]}')

        # Crear y enviar el mensaje
        message = f'sumar {num1} {num2}'.encode()
        sock.sendall(f"{len(message):05d}".encode() + message)
        print(f'Solicitud enviada: sumar {num1} {num2}')

        # Esperar la respuesta
        header = sock.recv(5).decode()
        response_length = int(header)
        response = sock.recv(response_length).decode()

        print(f'Respuesta recibida: {response}')

if __name__ == "__main__":
    num1 = int(input("Introduce el primer número: "))
    num2 = int(input("Introduce el segundo número: "))
    send_sum_request(num1, num2)
