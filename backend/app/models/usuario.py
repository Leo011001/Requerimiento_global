from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default="alumno")  # admin | bibliotecario | alumno
    activo = db.Column(db.Boolean, default=True)  # baja lógica
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    prestamos = db.relationship("Prestamo", backref="usuario", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "tipo": self.tipo,
            "activo": self.activo,
            "fecha_registro": self.fecha_registro.isoformat(),
        }
