# Ejercicios: Vistas y Rutas

## Ejercicio 1: Crear una vista para mostrar vacantes
Crea una función de vista que muestre todas las vacantes en la base de datos y las pase a una plantilla.

### Ejemplo:
```python
@app.route('/vacantes')
def mostrar_vacantes():
    vacantes = Vacante.query.all()
    return render_template('vacantes.html', vacantes=vacantes)
```

## Ejercicio 2: Vista de detalle
Crea una vista que muestre el detalle de una vacante seleccionada por su id.

### Ejemplo:
```python
@app.route('/vacante/<int:id>')
def detalle_vacante(id):
    vacante = Vacante.query.get_or_404(id)
    return render_template('detalle.html', vacante=vacante)
```

## Reto
Agrega una ruta que permita filtrar vacantes por categoría.
