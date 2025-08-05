from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import Usuario
from werkzeug.security import check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('main.admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html', datetime=datetime)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.index'))
