"""
PATRÓN MEDIATOR:
`BibliotecaMediator` centraliza la comunicación entre los servicios de
Usuario, Libro y Prestamo. En lugar de que PrestamoService hable
directamente con LibroService y UsuarioService (acoplamiento fuerte),
todos pasan por el mediador, que orquesta el flujo y mantiene las reglas
de negocio en un solo lugar.
"""
from app import db
from app.models import Usuario, Libro, Prestamo
from app.patterns.builders import PrestamoBuilder
from datetime import datetime


class BibliotecaMediator:
    def solicitar_prestamo(self, usuario_id: int, libro_id: int, dias: int = 7) -> Prestamo:
        usuario = Usuario.query.get(usuario_id)
        libro = Libro.query.get(libro_id)

        if not usuario or not usuario.activo:
            raise ValueError("Usuario no encontrado o inactivo")
        if not libro or not libro.activo:
            raise ValueError("Libro no encontrado o inactivo")
        if libro.copias_disponibles < 1:
            raise ValueError("No hay copias disponibles de este libro")

        prestamo = (
            PrestamoBuilder()
            .para_usuario(usuario_id)
            .del_libro(libro_id)
            .por_dias(dias)
            .build()
        )

        libro.copias_disponibles -= 1
        db.session.add(prestamo)
        db.session.commit()
        return prestamo

    def registrar_devolucion(self, prestamo_id: int) -> Prestamo:
        prestamo = Prestamo.query.get(prestamo_id)
        if not prestamo:
            raise ValueError("Préstamo no encontrado")
        if prestamo.estado == "devuelto":
            raise ValueError("Este préstamo ya fue devuelto")

        prestamo.fecha_devolucion_real = datetime.utcnow()
        prestamo.estado = "devuelto"

        libro = Libro.query.get(prestamo.libro_id)
        libro.copias_disponibles += 1

        db.session.commit()
        return prestamo
