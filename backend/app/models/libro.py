from app import db


class Libro(db.Model):
    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    categoria = db.Column(db.String(80))
    copias_totales = db.Column(db.Integer, default=1)
    copias_disponibles = db.Column(db.Integer, default=1)
    activo = db.Column(db.Boolean, default=True)  # baja lógica

    prestamos = db.relationship("Prestamo", backref="libro", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "categoria": self.categoria,
            "copias_totales": self.copias_totales,
            "copias_disponibles": self.copias_disponibles,
            "activo": self.activo,
        }
