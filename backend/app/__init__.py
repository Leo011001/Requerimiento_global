"""
Inicialización de la app Flask.

PATRÓN SINGLETON:
La instancia de SQLAlchemy (`db`) se crea una sola vez en este módulo y se
importa en todo el resto de la aplicación. Flask-SQLAlchemy garantiza que
solo exista una conexión/engine compartido para toda la app, evitando
múltiples instancias de conexión a la base de datos.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()           # Singleton: única instancia de acceso a datos
jwt = JWTManager()          # Maneja autenticación por tokens


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biblioteca.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "cambia-esta-clave-en-produccion"

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # Registro de blueprints (rutas)
    from app.routes.auth_routes import auth_bp
    from app.routes.usuario_routes import usuario_bp
    from app.routes.libro_routes import libro_bp
    from app.routes.prestamo_routes import prestamo_bp
    from app.routes.reporte_routes import reporte_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(usuario_bp, url_prefix="/api/usuarios")
    app.register_blueprint(libro_bp, url_prefix="/api/libros")
    app.register_blueprint(prestamo_bp, url_prefix="/api/prestamos")
    app.register_blueprint(reporte_bp, url_prefix="/api/reportes")

    with app.app_context():
        db.create_all()

    return app
