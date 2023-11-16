
def menuCliente(nombre, rol, token):
    while True:
        print(f"""
        Bienvenido {rol} {nombre}
        1. Reservar una hora
        2. Salir
        \n
        token: {token}
        _________________________________________________________
        """)
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            print("Reservar una hora")
        elif opcion == "2":
            print("Has salido del menú cliente")
            return
