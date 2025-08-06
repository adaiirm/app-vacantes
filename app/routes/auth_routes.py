from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# Importa el modelo de usuario
from ..models import Usuario
# Para verificar contraseñas
from werkzeug.security import check_password_hash
# Para mostrar fecha/hora en plantillas
from datetime import datetime

auth_bp = Blueprint('auth', __name__)  # Blueprint para rutas de autenticación

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Vista para iniciar sesión.
    Verifica credenciales y crea sesión si son correctas.
    """
    if request.method == 'POST':
        username = request.form.get('user')  # Obtiene usuario del formulario
        password = request.form.get('pass')  # Obtiene contraseña del formulario

        usuario = Usuario.query.filter_by(username=username).first()  # Busca usuario en la base de datos

        if usuario and check_password_hash(usuario.password, password):
            # Si las credenciales son correctas, guarda datos en la sesión
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            session['perfil'] = usuario.perfil
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    # Renderiza el formulario de login
    return render_template('login.html', datetime=datetime)

@auth_bp.route('/logout')
def logout():
    """
    Vista para cerrar sesión.
    Limpia la sesión y redirige al inicio.
    """
    session.clear()  # Elimina todos los datos de la sesión
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.index'))
