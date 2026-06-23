from flask import Blueprint, jsonify
from app.patterns.reportes import (
    ReporteLibrosPrestados,
    ReporteLibrosDisponibles,
    ReporteUsuariosConPrestamosActivos,
)

reporte_bp = Blueprint("reportes", __name__)


@reporte_bp.get("/libros-prestados")
def reporte_libros_prestados():
    return jsonify(ReporteLibrosPrestados().generar())


@reporte_bp.get("/libros-disponibles")
def reporte_libros_disponibles():
    return jsonify(ReporteLibrosDisponibles().generar())


@reporte_bp.get("/usuarios-con-prestamos")
def reporte_usuarios_con_prestamos():
    return jsonify(ReporteUsuariosConPrestamosActivos().generar())
