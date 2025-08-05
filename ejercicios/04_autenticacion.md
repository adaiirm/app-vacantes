# Ejercicios: Autenticación de Usuarios

## Ejercicio 1: Crear formulario de login
Crea un formulario para que los usuarios puedan iniciar sesión con email y contraseña.

### Ejemplo:
```html
<form method="post">
  <input type="email" name="email" required>
  <input type="password" name="password" required>
  <button type="submit">Iniciar sesión</button>
</form>
```

## Ejercicio 2: Validar credenciales
En la vista, valida que el usuario exista y que la contraseña sea correcta.

### Ejemplo:
```python
usuario = Usuario.query.filter_by(email=email).first()
if usuario and check_password_hash(usuario.password, password):
    # Login exitoso
else:
    flash('Credenciales incorrectas')
```

## Reto
Agrega una funcionalidad para cerrar sesión.
