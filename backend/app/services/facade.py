"""
PATRÓN FACADE:
`BibliotecaFacade` ofrece una interfaz simple y unificada para las
operaciones más comunes del sistema, ocultando los detalles de validación,
construcción de objetos (Builder) y persistencia. Las rutas Flask llaman
a la fachada en lugar de manejar directamente SQLAlchemy y los builders.
"""
from app import db
from app.models import Usuario, Libro
from app.patterns.builders import UsuarioBuilder


class BibliotecaFacade:
    # ---------- Usuarios ----------
    def crear_usuario(self, nombre, correo, password, tipo="alumno"):
        usuario = (
            UsuarioBuilder()
            .con_nombre(nombre)
            .con_correo(correo)
            .con_password(password)
            .con_tipo(tipo)
            .build()
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def listar_usuarios(self, solo_activos=True):
        query = Usuario.query
        if solo_activos:
            query = query.filter_by(activo=True)
        return query.all()

    def actualizar_usuario(self, usuario_id, **campos):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        for campo, valor in campos.items():
            if hasattr(usuario, campo) and campo != "id":
                setattr(usuario, campo, valor)
        db.session.commit()
        return usuario

    def dar_baja_usuario(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        usuario.activo = False
        db.session.commit()
        return usuario

    # ---------- Libros ----------
    def registrar_libro(self, titulo, autor, isbn, categoria="", copias=1):
        if Libro.query.filter_by(isbn=isbn).first():
            raise ValueError("Ya existe un libro con ese ISBN")
        libro = Libro(
            titulo=titulo, autor=autor, isbn=isbn,
            categoria=categoria, copias_totales=copias, copias_disponibles=copias,
        )
        db.session.add(libro)
        db.session.commit()
        return libro

    def listar_libros(self, solo_activos=True):
        query = Libro.query
        if solo_activos:
            query = query.filter_by(activo=True)
        return query.all()

    def actualizar_libro(self, libro_id, **campos):
        libro = Libro.query.get(libro_id)
        if not libro:
            raise ValueError("Libro no encontrado")
        for campo, valor in campos.items():
            if hasattr(libro, campo) and campo != "id":
                setattr(libro, campo, valor)
        db.session.commit()
        return libro

    def dar_baja_libro(self, libro_id):
        libro = Libro.query.get(libro_id)
        if not libro:
            raise ValueError("Libro no encontrado")
        libro.activo = False
        db.session.commit()
        return libro
