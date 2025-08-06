from flask import Flask
# Importa el modelo de base de datos y usuario
from .models import db, Usuario
# Para generar contraseñas seguras
from werkzeug.security import generate_password_hash
# Para manejo de rutas y archivos
import os

def create_app():
    """
    Función principal para crear y configurar la aplicación Flask.
    Incluye configuración de base de datos, registro de blueprints y creación de usuario admin por defecto.
    """
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # Clave secreta para sesiones

    # Configuración de la base de datos SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'mycompany.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Inicializa la base de datos con la app

    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        # Crea el usuario admin por defecto si no existe
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(
                username='admin',
                email='admin@mycompany.com',
                password=generate_password_hash('admin123'),
                perfil='Administrador',
                estatus='Activo'
            )
            db.session.add(admin)
            db.session.commit()

    # Registrar blueprints para separar rutas por funcionalidad
    from .routes.auth_routes import auth_bp  # Rutas de autenticación
    from .routes.main_routes import main_bp  # Rutas principales
    from .routes.vacante_routes import vacante_bp  # Rutas de vacantes

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(vacante_bp)

    return app
