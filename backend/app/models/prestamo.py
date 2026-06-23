from datetime import datetime
from app import db


class Prestamo(db.Model):
    __tablename__ = "prestamos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id"), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(20), default="activo")  # activo | devuelto | atrasado

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "libro_id": self.libro_id,
            "fecha_prestamo": self.fecha_prestamo.isoformat(),
            "fecha_devolucion_esperada": self.fecha_devolucion_esperada.isoformat(),
            "fecha_devolucion_real": self.fecha_devolucion_real.isoformat() if self.fecha_devolucion_real else None,
            "estado": self.estado,
        }
