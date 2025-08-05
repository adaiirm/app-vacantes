from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Usuario, Vacante
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_bootstrap import Bootstrap5

import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = os.urandom(24)

# Configuración de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mycompany.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas en la base de datos
with app.app_context():
    db.create_all()
    # Crear usuario admin si no existe
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            email='admin@mycompany.com',
            password=generate_password_hash('admin123'),
            perfil='Administrador',
            estatus='Activo'
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).limit(3).all()
    return render_template('index.html', vacantes=vacantes, datetime=datetime)

@app.route('/acerca')
def acerca():
    return render_template('acerca.html', datetime=datetime)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.password, password):
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            session['perfil'] = usuario.perfil
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html', datetime=datetime)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['user_id'])
    return render_template('admin.html', usuario=usuario, datetime=datetime)

@app.route('/vacantes')
def vacantes():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('login'))
    
    todas_vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).all()
    return render_template('vacantes.html', vacantes=todas_vacantes, datetime=datetime, mensaje=None)

@app.route('/vacante/nueva', methods=['GET', 'POST'])
def nueva_vacante():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        detalle = request.form.get('detalle')
        
        if not nombre or not descripcion:
            flash('Todos los campos son obligatorios', 'danger')
        else:
            nueva_vacante = Vacante(
                nombre=nombre,
                descripcion=descripcion,
                detalle=detalle,
                fecha_publicacion=datetime.now(),
                usuario_id=session['user_id']
            )
            db.session.add(nueva_vacante)
            db.session.commit()
            flash('Vacante creada exitosamente', 'success')
            return redirect(url_for('vacantes'))
    
    return render_template('frmvacante.html', datetime=datetime)

@app.route('/vacante/<int:id>')
def detalle_vacante(id):
    vacante = Vacante.query.get_or_404(id)
    return render_template('detalle.html', vacante=vacante, datetime=datetime)

@app.route('/vacante/eliminar/<int:id>')
def eliminar_vacante(id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('login'))
    
    vacante = Vacante.query.get_or_404(id)
    db.session.delete(vacante)
    db.session.commit()
    flash('Vacante eliminada exitosamente', 'success')
    return redirect(url_for('vacantes'))

@app.route('/buscar')
def buscar():
    query = request.args.get('query', '')
    if query:
        resultados = Vacante.query.filter(Vacante.nombre.contains(query) | Vacante.query.filter(Vacante.descripcion.contains(query)))
        resultados = resultados.order_by(Vacante.fecha_publicacion.desc()).all()
    else:
        resultados = []
    
    return render_template('vacantes.html', vacantes=resultados, busqueda=query, datetime=datetime, mensaje=None)

# Añade estas rutas adicionales al final de tu app.py

@app.route('/mensaje')
def mostrar_mensaje():
    tipo = request.args.get('tipo', 'info')
    titulo = request.args.get('titulo', 'Mensaje del Sistema')
    contenido = request.args.get('contenido', '')
    detalles = request.args.get('detalles', '')
    enlace = request.args.get('enlace', '')
    texto_enlace = request.args.get('texto_enlace', 'Volver')
    
    mensaje = {
        'tipo': tipo,
        'titulo': titulo,
        'contenido': contenido,
        'detalles': detalles,
        'enlace': enlace,
        'texto_enlace': texto_enlace
    }
    
    return render_template('mensaje.html', mensaje=mensaje, datetime=datetime)

@app.route('/vacante/editar', methods=['GET', 'POST'])
def editar_vacante():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('login'))
    
    vacante_id = request.args.get('edit') or request.form.get('vacante_id')
    if not vacante_id:
        flash('No se especificó la vacante a editar', 'danger')
        return redirect(url_for('vacantes'))
    
    vacante = Vacante.query.get_or_404(vacante_id)
    
    if vacante.usuario_id != session['user_id']:
        flash('No tienes permiso para editar esta vacante', 'danger')
        return redirect(url_for('vacantes'))
    
    if request.method == 'POST':
        vacante.nombre = request.form.get('nombre')
        vacante.descripcion = request.form.get('descripcion')
        vacante.detalle = request.form.get('detalle')
        vacante.fecha_publicacion = datetime.now()
        
        db.session.commit()
        flash('Vacante actualizada exitosamente', 'success')
        return redirect(url_for('detalle_vacante', id=vacante.id))
    
    return render_template('frmvacante.html', vacante=vacante, edit_mode=True, datetime=datetime)

if __name__ == '__main__':
    app.run(debug=True)