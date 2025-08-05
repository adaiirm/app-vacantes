from flask import Flask
from .models import db, Usuario
from werkzeug.security import generate_password_hash
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Configuración base de datos
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'mycompany.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
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

    # Registrar blueprints
    from .routes.auth_routes import auth_bp
    from .routes.main_routes import main_bp
    from .routes.vacante_routes import vacante_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(vacante_bp)

    return app
