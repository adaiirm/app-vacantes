from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, Vacante
from datetime import datetime

vacante_bp = Blueprint('vacante', __name__)

@vacante_bp.route('/vacantes')
def vacantes():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'warning')
        return redirect(url_for('auth.login'))

    todas_vacantes = Vacante.query.order_by(Vacante.fecha_publicacion.desc()).all()
    return render_template('vacantes.html', vacantes=todas_vacantes, datetime=datetime, mensaje=None)

@vacante_bp.route('/vacante/nueva', methods=['GET', 'POST'])
def nueva_vacante():
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

    return render_template('frmvacante.html', datetime=datetime)

@vacante_bp.route('/vacante/<int:id>')
def detalle_vacante(id):
    vacante = Vacante.query.get_or_404(id)
    return render_template('detalle.html', vacante=vacante, datetime=datetime)

@vacante_bp.route('/vacante/eliminar/<int:id>')
def eliminar_vacante(id):
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

    return render_template('frmvacante.html', vacante=vacante, edit_mode=True, datetime=datetime)

@vacante_bp.route('/buscar')
def buscar():
    query = request.args.get('query', '')
    if query:
        resultados = Vacante.query.filter(
            Vacante.nombre.contains(query) | Vacante.descripcion.contains(query)
        ).order_by(Vacante.fecha_publicacion.desc()).all()
    else:
        resultados = []

    return render_template('vacantes.html', vacantes=resultados, busqueda=query, datetime=datetime, mensaje=None)

@vacante_bp.route('/mensaje')
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
