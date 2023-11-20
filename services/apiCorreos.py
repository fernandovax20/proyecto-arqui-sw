from flask import Flask, request, jsonify, render_template, redirect, url_for
import busConnect as bc
import os

# Obtener la ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Establecer la ruta de la carpeta templates
ruta_templates = os.path.join(directorio_actual, '..', 'templates')

app = Flask(__name__, template_folder=ruta_templates)

@app.route('/')
def index():
    return '¡La API está funcionando!'

@app.route('/api', methods=['GET'])
def api():
    # Extrae el valor de id_reserva de la cadena de consulta
    id_reserva = request.args.get('id_reserva')

    bc.sendToBus("dbcon", {"instruccion": "procesarConfirmacionesReserva", "id_reserva": int(id_reserva)})

    # Haz lo que necesites con el valor de id_reserva (almacenarlo, procesarlo, etc.)
    resultado = f'Hemos Confirmado la reserva con id: {id_reserva}'
    print('Hemos confirmado la reserva con id:', id_reserva)

    return resultado

@app.route('/mostrar-formulario/<int:id_reserva>')
def mostrar_formulario(id_reserva):
    # Pasar id_reserva a la plantilla
    return render_template('formulario.html', id_reserva=id_reserva)

@app.route('/formulario', methods=['POST'])
def formulario():
    if request.method == 'POST':
        # Extrae los datos del formulario
        id_reserva = request.form.get('id_reserva')
        valoracion = request.form.get('valoracion')
        comment = request.form.get('comment')

        bc.sendToBus("dbcon", {
            "instruccion": "guardarFeedback", 
            "id_reserva": int(id_reserva), 
            "valoracion": valoracion, 
            "comentarios": comment
        })

        return redirect(url_for('exito'))
    
@app.route('/exito')
def exito():
    return "Formulario procesado correctamente"

if __name__ == '__main__':
    # Define el puerto en el que escuchará la API (por ejemplo, el puerto 5000)
    puerto = 5001

    # Inicia la aplicación Flask
    app.run(debug=True, port=puerto)
