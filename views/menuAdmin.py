from views import viewLogic as vl
from helpers import validadores as val
import pwinput

def menuAdmin(nombre, rol, token):

    while True:
        print(f"""
        Bienvenido {rol} {nombre}
        1. Administrar Servicios
        2. Administrar Usuarios
        3. Administrar Reservas
        4. Salir
        \n
        token: {token}
        _________________________________________________________
        """)
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            while True:
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
                    nombre = val.validar_nombre_servicio()
                    precio = val.validar_precio_servicio()
                    puntos_por_servicio = val.validar_puntos_por_servicio()
                    res = vl.CrearServicio(token, nombre, precio,puntos_por_servicio)
                    print("\n"+res["data"])
                elif opcion == "3":
                    print("Editar Servicio")
                    arr_ids = vl.ListarServicios()
                    print("ingresa el id del servicio a editar")
                    id = val.validar_id_servicio(arr_ids)
                    nombre = val.validar_nombre_servicio()
                    precio = val.validar_precio_servicio()
                    puntos_por_servicio = val.validar_puntos_por_servicio()
                    res = vl.editarServicio(token, id, nombre, precio, puntos_por_servicio)
                    print("\n"+res["data"])
                elif opcion == "4":
                    print("Eliminar Servicio")
                    arr_ids = vl.ListarServicios()
                    print("ingresa el id del servicio a eliminar")
                    id = val.validar_id_servicio(arr_ids)
                    res = vl.eliminarServicio(token, id)
                    print("\n"+res["data"])
                elif opcion == "5":
                    print("Has salido del menú administrador")
                    break
                else:
                    print("Opción no válida")

        elif opcion == "2":
            print("Administrar Usuarios")

            while True:
                print(f"""
                        Que desea hacer {rol} {nombre} ?
                        1. Listar Usuarios
                        2. Crear Usuario
                        3. Editar Usuario
                        4. Eliminar Usuario
                        5. Salir
                        \n
                        token: {token}
                        _________________________________________________________
                """)

                opcion = input("Ingrese opción: ")
                if opcion == "1":
                    print("Listar Usuarios")
                    vl.ListarUsuarios(token)
                elif opcion == "2":
                    print("Crear Usuario")
                    nombre = val.obtener_nombre_valido()
                    email = val.obtener_email_valido()
                    password = pwinput.pwinput("Ingrese su contraseña: ")
                    role = val.validar_role_usuario()
                    res = vl.crearUsuario(token, nombre, email, password, role)
                    print("\n"+res["data"])
                elif opcion == "3":
                    print("Editar Usuario")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario a editar")
                    id = val.validar_id_usuario(users)
                    usuario_a_editar = next((user for user in users if user["id"] == id), None)

                    if usuario_a_editar:
                        print(f"Nombre actual: {usuario_a_editar['nombre']}")
                        nuevo_nombre = val.obtener_nombre_valido() if input("¿Desea cambiar el nombre? (s/n): ").lower() == 's' else usuario_a_editar['nombre']

                        print(f"Email actual: {usuario_a_editar['email']}")
                        nuevo_email = val.obtener_email_valido() if input("¿Desea cambiar el email? (s/n): ").lower() == 's' else usuario_a_editar['email']

                        nueva_password = pwinput.pwinput("Ingresa la nueva contraseña o presiona Enter para mantener la actual: ")
                        nueva_password = nueva_password if nueva_password else None  

                        print(f"Rol actual: {usuario_a_editar['nombre_rol']}")
                        nuevo_rol = val.validar_role_usuario() if input("¿Desea cambiar el rol? (s/n): ").lower() == 's' else usuario_a_editar['nombre_rol']
                        

                        res = vl.editarUsuario(token, id, nuevo_nombre, nuevo_email, nueva_password, nuevo_rol)
                        
                        print("\n"+res["data"])
                    else:
                        print("Usuario no encontrado.")

                elif opcion == "4":
                    print("Eliminar Usuario")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario a eliminar")
                    id = val.validar_id_usuario(users)
                    res = vl.eliminarUsuario(token, id)
                    print("\n"+res["data"])
                elif opcion == "5":
                    print("Has salido del menú administrador")
                    break
                else:
                    print("Opción no válida")

        elif opcion == "3":
            print("Administrar Reservas")

            while True:
                print(f"""
                        Que desea hacer {rol} {nombre} ?
                        1. Listar Reservas
                        2. Listar Reservas por usuario
                        3. Crear Reserva
                        4. Editar Reserva
                        5. Eliminar Reserva
                        6. Confirmar asistencia
                        7. Salir
                        \n
                        token: {token}
                        _________________________________________________________
                """)

                opcion = input("Ingrese opción: ")
                if opcion == "1":
                    print("Listar Reservas")
                    vl.ListarReservas(token)
                elif opcion == "2":
                    print("Listar reserva por usuario")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario para el cual se editara la reserva")
                    id_usuario = val.validar_id_usuario(users)
                    id_reserva = vl.reservasPorUserId(token, id_usuario, False)

                elif opcion == "3":
                    print("Crear Reserva")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario para el cual se creará la reserva")
                    id_usuario = val.validar_id_usuario(users)

                    print("Lista de Servicios")
                    arr_ids = vl.ListarServicios()
                    print("ingresa el id del servicio a reservar")
                    id_servicio = val.validar_id_servicio(arr_ids)
                    print("ingresa la fecha de la reserva")
                    fecha_hora_utc=vl.mostrar_calendario()
                    res = vl.crearReserva(token, id_usuario, id_servicio, fecha_hora_utc)
                    print("\n"+res["data"])


                elif opcion == "4":
                    print("Editar Reserva")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario para el cual se editara la reserva")
                    id_usuario = val.validar_id_usuario(users)
                    id_reserva = vl.reservasPorUserId(token, id_usuario)
                    print("Lista de Servicios")
                    arr_ids = vl.ListarServicios()
                    print("ingresa el id del servicio a reservar")
                    id_servicio = val.validar_id_servicio(arr_ids)
                    print("ingresa la fecha de la reserva")
                    fecha_hora_utc=vl.mostrar_calendario()
                    res = vl.updateReserva(token, id_reserva, id_usuario, id_servicio, fecha_hora_utc)
                    print("\n"+res["data"])

                elif opcion == "5":
                    print("Eliminar Reserva")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario para el cual se eliminara la reserva")
                    id_usuario = val.validar_id_usuario(users)
                    id_reserva = vl.reservasPorUserId(token, id_usuario)
                    res = vl.deleteReserva(token, id_reserva)
                    print("\n"+res["data"])
                
                elif opcion == "6":
                    print("Confirmar asistencia")
                    users = vl.ListarUsuarios(token)
                    print("ingresa el id del usuario para el cual se confirmará la asistencia")
                    id_usuario = val.validar_id_usuario(users)
                    id_reserva = vl.reservasPorUserId(token, id_usuario)
                    res = vl.ConfirmarAsistencia(token, id_reserva)
                    print("\n"+res["data"])

                elif opcion == "7":
                    print("Has salido del menú administrador")
                    break
                else:
                    print("Opción no válida")

        elif opcion == "4":
            print("Has salido del menú administrador")
            return
