import socket
import sys
import time 
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
    
def GlobalServiceConnect(nombre, funcion):
    caracteres = "El nombre debe tener 5 caracteres justos"
    if(len(nombre) > 5):
        return caracteres
    elif(len(nombre) < 5 or len(nombre) == 0):
        return caracteres
    
    # Create a TCP/IP socket
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5000)
    print ('connecting to {} port {}'.format (*server_address))
    sock.connect (server_address)

    try:
        # Send data
        message = b'00011sinit'+nombre.encode('utf-8')
        print ('sending {!r}'.format (message))
        sock.sendall (message)

        amount_received = 0
        amount_expected = int(sock.recv (5))
        while amount_received < amount_expected:
            data = sock.recv (amount_expected - amount_received)
            amount_received += len (data)
            print('received {!r}'.format(data))

        while True:
            print ("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv (5))

            while amount_received < amount_expected:
                data = sock.recv (amount_expected - amount_received)
                amount_received += len (data)
                print('received {!r}'.format(data))
        
            print ("Processing ...")
            print(data.decode())
            ndata = funcion(data.decode())

            resp='{:05d}'.format (len(ndata) + 5) + nombre + ndata
            
            print ("Send answer (if needed)")
            print ('sending {}'.format (resp))
            sock.sendall (bytes(resp, 'utf-8'))

    finally:
        print ('closing socket')
        sock.close ()


