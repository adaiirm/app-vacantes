from flask_sqlalchemy import SQLAlchemy
# Importa funciones para manejo seguro de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash
# Importa clase para manejar fechas
from datetime import datetime

db = SQLAlchemy()  # Instancia principal para manejar la base de datos

class Usuario(db.Model):
    """
    Modelo para usuarios del sistema.
    Almacena información básica y credenciales.
    """
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos
    
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    username = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario
    email = db.Column(db.String(100), unique=True, nullable=False)  # Correo electrónico
    password = db.Column(db.String(200), nullable=False)  # Contraseña encriptada
    perfil = db.Column(db.String(50), nullable=False, default='Usuario')  # Rol del usuario
    estatus = db.Column(db.String(20), nullable=False, default='Activo')  # Estado del usuario
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Fecha de registro
    vacantes = db.relationship('Vacante', backref='autor', lazy=True)  # Relación con vacantes creadas
    
    def set_password(self, password):
        """Genera y almacena el hash de la contraseña."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña proporcionada es correcta."""
        return check_password_hash(self.password, password)

class Vacante(db.Model):
    """
    Modelo para vacantes publicadas por los usuarios.
    Almacena información relevante de cada vacante.
    """
    __tablename__ = 'vacantes'  # Nombre de la tabla en la base de datos
    
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    nombre = db.Column(db.String(100), nullable=False)  # Título de la vacante
    descripcion = db.Column(db.Text, nullable=False)  # Descripción general
    detalle = db.Column(db.Text)  # Detalles adicionales
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Fecha de publicación
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # Autor de la vacante
    
    def __repr__(self):
        """Representación legible de la vacante."""
        return f'<Vacante {self.nombre}>'