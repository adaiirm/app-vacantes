# Ejercicios: Plantillas y Herencia

## Ejercicio 1: Crear una plantilla base
Crea una plantilla `base.html` con bloques para el título y el contenido.

### Ejemplo:
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <title>{% block titulo %}Mi App{% endblock %}</title>
</head>
<body>
  {% block contenido %}{% endblock %}
</body>
</html>
```

## Ejercicio 2: Heredar la plantilla base
Crea una plantilla que herede de `base.html` y muestre una lista de vacantes.

### Ejemplo:
```html
{% extends 'base.html' %}
{% block titulo %}Vacantes{% endblock %}
{% block contenido %}
  <ul>
    {% for vacante in vacantes %}
      <li>{{ vacante.titulo }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```

## Reto
Agrega un bloque para mensajes flash en la plantilla base.
