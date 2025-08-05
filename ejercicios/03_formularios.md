# Ejercicios: Formularios y Validaciones

## Ejercicio 1: Crear un formulario de registro de vacante
Crea un formulario en HTML para registrar una nueva vacante con los campos: título, descripción y categoría.

### Ejemplo:
```html
<form method="post">
  <input type="text" name="titulo" required>
  <textarea name="descripcion" required></textarea>
  <select name="categoria_id">
    <!-- Opciones de categorías -->
  </select>
  <button type="submit">Registrar</button>
</form>
```

## Ejercicio 2: Validar datos en la vista
Valida en la vista que el título y la descripción no estén vacíos antes de guardar la vacante.

### Ejemplo:
```python
if request.method == 'POST':
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    if not titulo or not descripcion:
        flash('Todos los campos son obligatorios')
```

## Reto
Agrega validación para que el título tenga al menos 5 caracteres.
