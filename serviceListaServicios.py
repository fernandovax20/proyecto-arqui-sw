import json

ListaServicios = {
    "servicios": [
        "Corte de cabello",
        "Afeitado de barba",
        "Corte de cabello y barba",
        "Corte de cabello y afeitado de barba",
        "Corte de cabello, barba y cejas",
    ]
}

def ListarServicios(data=None):
    json_string = json.dumps(ListaServicios)
    respuesta = json_string
    return respuesta