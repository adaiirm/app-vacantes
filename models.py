from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.String(50), nullable=False, default='Usuario')
    estatus = db.Column(db.String(20), nullable=False, default='Activo')
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now)
    vacantes = db.relationship('Vacante', backref='autor', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Vacante(db.Model):
    __tablename__ = 'vacantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    detalle = db.Column(db.Text)
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def __repr__(self):
        return f'<Vacante {self.nombre}>'