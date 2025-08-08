from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# Importa modelo y base de datos
from ..models import db, Vacante
# Para mostrar fecha/hora en plantillas
from datetime import datetime

vacante_bp = Blueprint('vacante', __name__)  # Blueprint para rutas de vacantes

@vacante_bp.route('/vacantes')
def vacantes():
    """
    Vista para mostrar todas las vacantes.
    Solo accesible para usuarios autenticados.
    """
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    todas_vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).all()
    return render_template('vacantes.html', vacantes=todas_vacantes, mensaje=None)

# Ruta pública para ver todas las vacantes sin credenciales
@vacante_bp.route('/todas_vacantes')
def todas_vacantes():
    """
    Vista pública para mostrar todas las vacantes sin requerir inicio de sesión.
    """
    vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).all()
    return render_template('todas_vacantes.html', vacantes=vacantes)

@vacante_bp.route('/vacante/nueva', methods=['GET', 'POST'])
def nueva_vacante():
    """
    Vista para crear una nueva vacante.
    Solo accesible para usuarios autenticados.
    """
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        detalle = request.form.get('detalle')

        if not nombre or not descripcion:
            flash('Todos los campos son obligatorios', 'danger')
        else:
            nueva = Vacante(
                nombre=nombre,
                descripcion=descripcion,
                detalle=detalle,
                fecha_publicacion=datetime.now(),
                usuario_id=session['user_id']
            )
            db.session.add(nueva)
            db.session.commit()
            flash('Vacante creada exitosamente', 'success')
            return redirect(url_for('vacante.vacantes'))

    return render_template('frmvacante.html')

@vacante_bp.route('/vacante/<int:id>')
def detalle_vacante(id):
    """
    Vista para mostrar el detalle de una vacante específica.
    """
    vacante = Vacante.query.get_or_404(id)
    return render_template('detalle.html', vacante=vacante)

@vacante_bp.route('/vacante/eliminar/<int:id>')
def eliminar_vacante(id):
    """
    Vista para eliminar una vacante.
    Solo accesible para usuarios autenticados.
    """
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    vacante = Vacante.query.get_or_404(id)
    db.session.delete(vacante)
    db.session.commit()
    flash('Vacante eliminada exitosamente', 'success')
    return redirect(url_for('vacante.vacantes'))

@vacante_bp.route('/vacante/editar', methods=['GET', 'POST'])
def editar_vacante():
    """
    Vista para editar una vacante existente.
    Solo accesible para el autor de la vacante autenticado.
    """
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    vacante_id = request.args.get('edit') or request.form.get('vacante_id')
    if not vacante_id:
        flash('No se especificó la vacante a editar', 'danger')
        return redirect(url_for('vacante.vacantes'))

    vacante = Vacante.query.get_or_404(vacante_id)

    if vacante.usuario_id != session['user_id']:
        flash('No tienes permiso para editar esta vacante', 'danger')
        return redirect(url_for('vacante.vacantes'))

    if request.method == 'POST':
        vacante.nombre = request.form.get('nombre')
        vacante.descripcion = request.form.get('descripcion')
        vacante.detalle = request.form.get('detalle')
        vacante.fecha_publicacion = datetime.now()

        db.session.commit()
        flash('Vacante actualizada exitosamente', 'success')
        return redirect(url_for('vacante.detalle_vacante', id=vacante.id))

    return render_template('frmvacante.html', vacante=vacante, edit_mode=True)

@vacante_bp.route('/buscar')
def buscar():
    """
    Vista para buscar vacantes por nombre o descripción.
    """
    query = request.args.get('query', '')
    if query:
        resultados = Vacante.query.filter(
            Vacante.nombre.contains(query) | Vacante.descripcion.contains(query)
        ).order_by(Vacante.fecha_publicacion.desc()).all()
    else:
        resultados = []

    return render_template('todas_vacantes.html', vacantes=resultados, busqueda=query, mensaje=None)

@vacante_bp.route('/mensaje')
def mostrar_mensaje():
    """
    Vista para mostrar mensajes personalizados en la aplicación.
    """
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

    return render_template('mensaje.html', mensaje=mensaje)
