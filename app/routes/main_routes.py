from flask import Blueprint, render_template, session, redirect, url_for, flash
# Importa modelos de vacante y usuario
from ..models import Vacante, Usuario
# Para mostrar fecha/hora en plantillas
from datetime import datetime

main_bp = Blueprint('main', __name__)  # Blueprint para rutas principales

@main_bp.route('/')
def index():
    """
    Vista principal (inicio).
    Muestra las 3 vacantes más recientes.
    """
    vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).limit(3).all()
    return render_template('index.html', vacantes=vacantes)

@main_bp.route('/acerca')
def acerca():
    """
    Vista de la página 'Acerca de'.
    """
    return render_template('acerca.html')

@main_bp.route('/admin')
def admin():
    """
    Vista del panel de administración.
    Solo accesible para usuarios autenticados.
    """
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get(session['user_id'])  # Obtiene el usuario actual
    return render_template('admin.html', usuario=usuario)
