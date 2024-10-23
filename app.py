from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta en producción

@app.route('/')
def index():
    productos = session.get('productos', [])
    # Ordenar los productos por ID (convertidos a entero)
    productos.sort(key=lambda x: int(x['id']))
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    nuevo_producto = {
    'id': request.form['id'],
    'nombre': request.form['nombre'],
    'cantidad': request.form['cantidad'],
    'precio': request.form['precio'],
    'fecha_vencimiento': request.form['fecha_vencimiento'],  # Asegúrate de incluir la fecha
    'categoria': request.form['categoria'],
}


    # Validar ID único
    productos = session.get('productos', [])
    for producto in productos:
        if producto['id'] == nuevo_producto['id']:
            return "El ID ya existe", 400

    productos.append(nuevo_producto)
    session['productos'] = productos
    return redirect(url_for('index'))

@app.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_producto(id):
    productos = session.get('productos', [])
    productos = [p for p in productos if p['id'] != id]
    session['productos'] = productos
    return redirect(url_for('index'))

@app.route('/editar/<string:id>', methods=['POST'])
def editar_producto(id):
    productos = session.get('productos', [])
    for producto in productos:
        if producto['id'] == id:
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = request.form['cantidad']
            producto['precio'] = request.form['precio']
            producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
            producto['categoria'] = request.form['categoria']
            break
    session['productos'] = productos
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)