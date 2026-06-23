"""
PATRÓN TEMPLATE METHOD:
`Reporte` define el esqueleto del algoritmo (`generar`) que siempre sigue
los mismos pasos: obtener datos, formatear y devolver. Las subclases solo
sobreescriben `obtener_datos`, sin tener que reescribir el flujo completo.
"""
from abc import ABC, abstractmethod
from app.models import Libro, Usuario, Prestamo


class Reporte(ABC):
    def generar(self) -> dict:
        datos = self.obtener_datos()
        return {
            "tipo": self.nombre(),
            "total": len(datos),
            "datos": datos,
        }

    @abstractmethod
    def obtener_datos(self) -> list:
        ...

    @abstractmethod
    def nombre(self) -> str:
        ...


class ReporteLibrosPrestados(Reporte):
    def nombre(self):
        return "libros_prestados"

    def obtener_datos(self):
        prestamos = Prestamo.query.filter_by(estado="activo").all()
        return [p.to_dict() for p in prestamos]


class ReporteLibrosDisponibles(Reporte):
    def nombre(self):
        return "libros_disponibles"

    def obtener_datos(self):
        libros = Libro.query.filter(Libro.copias_disponibles > 0, Libro.activo.is_(True)).all()
        return [l.to_dict() for l in libros]


class ReporteUsuariosConPrestamosActivos(Reporte):
    def nombre(self):
        return "usuarios_con_prestamos_activos"

    def obtener_datos(self):
        usuarios = (
            Usuario.query.join(Prestamo)
            .filter(Prestamo.estado == "activo")
            .distinct()
            .all()
        )
        return [u.to_dict() for u in usuarios]