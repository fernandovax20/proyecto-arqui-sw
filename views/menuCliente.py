from views import viewLogic as vl
from helpers import validadores as val

def menuCliente(nombre, rol, token):
    while True:
        print(f"""
        Bienvenido {rol} {nombre}
        1. Reservar una hora
        2. Mis reservas
        3. Mis Puntos
        4. Salir
        \n
        token: {token}
        _________________________________________________________
        """)
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            print("Reservar una hora")
            arr_ids = vl.ListarServicios()
            print("ingresa el id del servicio a reservar")
            id_servicio = val.validar_id_servicio(arr_ids)
            print("ingresa la fecha y hora de la reserva")
            fecha_hora_utc = vl.mostrar_calendario()

            res = vl.ReservarHora(token, id_servicio, fecha_hora_utc)
            print("\n"+res["data"])

        elif opcion == "2":
            print("Mis reservas")
            vl.MisReservas(token)
            
        elif opcion == "3":
            print("Mis puntos")
            vl.MisPuntos(token)

        elif opcion == "4":
            print("Saliendo...")
            break

