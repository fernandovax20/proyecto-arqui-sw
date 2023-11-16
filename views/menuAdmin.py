from views import viewLogic as vl

def menuAdmin(nombre, rol, token):

    while True:
        print(f"""
        Bienvenido {rol} {nombre}
        1. Administrar Servicios
        2. Administrar Usuarios
        3. Salir
        \n
        token: {token}
        _________________________________________________________
        """)
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            print("Administrar Servicios")
            print(f"""
                    Que desea hacer {rol} {nombre} ?
                    1. Listar Servicios
                    2. Crear Servicio
                    3. Editar Servicio
                    4. Eliminar Servicio
                    5. Salir
                    \n
                    token: {token}
                    _________________________________________________________
            """)

            opcion = input("Ingrese opción: ")
            if opcion == "1":
                print("Listar Servicios")
                vl.ListarServicios()
            elif opcion == "2":
                print("Crear Servicio")
                nombre = input("Ingrese nombre del servicio: ")
                description = input("Ingrese descripcion del servicio: ")
                precio = int(input("Ingrese precio del servicio: "))
                duracion = int(input("Ingrese duracion del servicio en minutos: "))
                puntos_por_servicio = int(input("Ingrese puntos por servicio: "))
                res = vl.CrearServicio(token, nombre, description, precio, duracion, puntos_por_servicio)
                print("\n"+res["data"])
            elif opcion == "3":
                print("Editar Servicio")
            elif opcion == "4":
                print("Eliminar Servicio")
                vl.ListarServicios()
                print("ingresa el id del servicio a eliminar")
                id = int(input("Ingrese id del servicio: "))
                res = vl.eliminarServicio(token, id)
                print("\n"+res["data"])
            elif opcion == "5":
                print("Has salido del menú administrador")
                return
            else:
                print("Opción no válida")

        elif opcion == "2":
            print("Administrar Usuarios")
        elif opcion == "3":
            print("Has salido del menú administrador")
            return
