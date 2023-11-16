from services import busConnect as bc
from views import menuPrincipal as mp
from views import menuCliente as mc
from views import menuAdmin as ma
import os
import sys

ruta_actual = os.path.realpath(__file__)
directorio_actual = os.path.dirname(ruta_actual)
directorio_raiz = os.path.dirname(directorio_actual)  
sys.path.append(directorio_raiz)


def verificar_token(token):
    """Verifica la validez de un token JWT."""
    res_dict = bc.sendToBus("svses", {"instruccion":"verify_token", "token":token})
    if res_dict["status"]:
        return res_dict["data"]["role"], res_dict["data"]["nombre"]
    else:
        return None, res_dict["data"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        rol, mensaje = verificar_token(token)

        if rol:
            if rol == "cliente":
                mc.menuCliente(mensaje, rol, token)
            elif rol == "admin":
                ma.menuAdmin(mensaje, rol, token)
            # Llamar al menú principal después de salir de menuCliente o menuAdmin
            mp.menuPrincipal()
        else:
            print("Error:", mensaje)
            mp.menuPrincipal()
    else:
        mp.menuPrincipal()

