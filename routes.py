from flask import Flask, render_template, request, redirect, url_for
import database 

app = Flask(__name__)

# --- 1. RUTA PRINCIPAL (CATÁLOGO REAL) ---
@app.route('/')
def catalogo():
    # available_dogs será una lista de tuplas de la DB
    dogs_from_db = database.get_available_dogs()
    return render_template('catalogo.html', dogs=dogs_from_db)

# --- 2. RUTA PARA MOSTRAR EL FORMULARIO ---
@app.route('/adoptar/<int:dog_id>')
def adoptar(dog_id):
    # perro será una tupla: (id, nombre, raza, edad)
    perro = database.get_dog_by_id(dog_id)
    if perro:
        # Pasamos el perro al template. 
        # En el HTML accederás a perro[1] para el nombre, perro[2] para raza, etc.
        return render_template('adoptar.html', dog=perro)
    return "Perrito no encontrado", 404

# --- 3. RUTA DEL HISTORIAL ---
@app.route('/historial')
def historial():
    # Trae la lista de adopciones exitosas
    adopciones = database.get_adoption_history()
    return render_template('historial.html', adopciones=adopciones)

# --- 4. RUTA PARA PROCESAR LA ADOPCIÓN ---
@app.route('/confirmar', methods=['POST'])
def confirmar():
    # Extraemos datos. Usamos .get() para evitar errores si falta un campo.
    dog_id = request.form.get('dog_id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    cedula = request.form.get('cedula')
    direccion = request.form.get('direccion')

    # Validación simple: que no haya campos vacíos
    if not all([dog_id, nombre, apellido, cedula, direccion]):
        return "<h1>❌ Error: Todos los campos son obligatorios.</h1><a href='/'>Volver</a>", 400

    # Ejecutamos la transacción
    exito = database.register_adoption_transactional(dog_id, nombre, apellido, direccion, cedula)

    if exito:
        return f"""
            <div style="text-align: center; font-family: sans-serif; margin-top: 50px; border: 2px solid #4caf50; padding: 20px; border-radius: 10px; display: inline-block; width: 80%;">
                <h1 style="color: #4caf50;">✅ ¡Adopción registrada con éxito!</h1>
                <p>Gracias <strong>{nombre} {apellido}</strong>.</p>
                <p>El perrito ha sido asignado a tu registro.</p>
                <br>
                <a href="/" style="background-color: #ff8a65; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Volver al catálogo</a>
                <a href="/historial" style="background-color: #4caf50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">Ver historial</a>
            </div>
        """
    else:
        return "<h1>❌ Error al procesar la adopción.</h1><p>Es posible que los datos ya existan o el servidor de MySQL no responda.</p><a href='/'>Volver</a>", 500

if __name__ == '__main__':
    app.run(debug=True)