from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')
app.secret_key = 'gabriel_hds'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'muebles_ventura'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# FUNCION DE LOGIN
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username = request.form['username']
        _password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE user = %s AND password = %s', (_username, _password,))
        account = cur.fetchone()

        if account:
            session['Inicio de Sesion Exitoso'] = True
            session['id_empleado'] = account['id_empleado']

            return render_template('admin.html')
        else:
            return render_template('index.html')

# Ruta para listar usuarios
@app.route('/usuarios')
def listar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=usuarios)

# Ruta para crear un nuevo usuario
@app.route('/crear-usuario', methods=['POST'])
def crear_usuario():
    if request.method == 'POST':
        _name = request.form['name']
        _last_name = request.form['last_name']
        _email = request.form['email']
        _username = request.form['user']
        _password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (name, last_name, email, user, password) VALUES (%s, %s, %s, %s, %s)",
                    (_name, _last_name, _email, _username, _password))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('listar_usuarios'))

# Ruta para editar un usuario existente
@app.route('/editar-usuario/<int:id>', methods=['POST'])
def editar_usuario(id):
    if request.method == 'POST':
        _name = request.form['name']
        _last_name = request.form['last_name']
        _email = request.form['email']
        _username = request.form['user']
        _password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET name = %s, last_name = %s, email = %s, user = %s, password = %s WHERE id = %s",
                    (_name, _last_name, _email, _username, _password, id))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('listar_usuarios'))



# Ruta para eliminar un usuario
@app.route('/eliminar-usuario/<int:id>')
def eliminar_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('listar_usuarios'))

# Ruta para ingresar pedidos
@app.route('/ingresar_pedidos', methods=['GET', 'POST'])
def ingresar_pedidos():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        direccion = request.form['direccion']
        fecha_entrega = request.form['fecha_entrega']
        tipo_madera = request.form['tipo_madera']
        acabado_pintura = request.form['acabado_pintura']
        tipo_cubierta = request.form['tipo_cubierta']
        boseleado = request.form['boseleado']

        # Conectar con la base de datos y guardar los datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ingreso_pedidos (nombre_cliente, apellido_cliente, direccion_cliente, fecha_ingreso, tipo_madera, acabado_pintura, tipo_cubierta, boseleado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nombres, apellidos, direccion, fecha_entrega, tipo_madera, acabado_pintura, tipo_cubierta, boseleado))
        mysql.connection.commit()
        cur.close()

        # Redirigir a una página de confirmación o a donde desees
        return redirect(url_for('admin'))

    return render_template('ingresar_pedidos.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)




 