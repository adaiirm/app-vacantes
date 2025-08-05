# Ejercicios Didácticos para el Proyecto "App Vacantes"

Bienvenido/a. En esta carpeta encontrarás ejercicios prácticos para aprender y practicar el desarrollo de este proyecto. Cada ejercicio incluye una breve explicación, instrucciones y retos para que puedas aplicar lo aprendido.

## Temas sugeridos
- Modelos y base de datos
- Vistas y rutas
- Formularios y validaciones
- Autenticación de usuarios
- Plantillas y herencia
- Estilos y recursos estáticos

Puedes crear un archivo por cada tema o seguir los ejemplos que aquí se proponen.

---

## Ejemplo de Ejercicio: Modelos y Base de Datos

### Objetivo
Aprender a crear y modificar modelos en SQLAlchemy y cómo reflejar los cambios en la base de datos.

### Instrucciones
1. Abre el archivo `models.py`.
2. Agrega un nuevo modelo llamado `Empresa` con los siguientes campos:
   - id (entero, clave primaria)
   - nombre (cadena, requerido)
   - direccion (cadena, opcional)
3. Crea una relación entre `Empresa` y las vacantes (una empresa puede tener muchas vacantes).
4. Explica cómo migrar los cambios a la base de datos.

### Reto
Agrega un método al modelo `Empresa` que devuelva la cantidad de vacantes asociadas.

---

Puedes agregar más ejercicios siguiendo este formato.
