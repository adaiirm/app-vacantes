from flask import Blueprint, render_template, session, redirect, url_for, flash
from ..models import Vacante, Usuario
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).limit(3).all()
    return render_template('index.html', vacantes=vacantes, datetime=datetime)

@main_bp.route('/acerca')
def acerca():
    return render_template('acerca.html', datetime=datetime)

@main_bp.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get(session['user_id'])
    return render_template('admin.html', usuario=usuario, datetime=datetime)
