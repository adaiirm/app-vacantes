# Ejercicios: Modelos y Base de Datos

## Ejercicio 1: Crear un modelo básico
Crea un modelo llamado `Categoria` con los campos `id` (entero, clave primaria) y `nombre` (cadena, requerido).

### Ejemplo:
```python
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
```

## Ejercicio 2: Relaciones uno a muchos
Agrega una relación entre `Categoria` y `Vacante` (una categoría puede tener muchas vacantes).

### Ejemplo:
```python
class Vacante(db.Model):
    # ...otros campos...
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref='vacantes')
```

## Reto
Agrega un método en `Categoria` que devuelva la cantidad de vacantes asociadas.
