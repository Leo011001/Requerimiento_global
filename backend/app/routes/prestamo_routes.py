from flask import Blueprint, request, jsonify
from app.patterns.mediator import BibliotecaMediator
from app.patterns.decorators import requiere_rol
from app.models import Prestamo

prestamo_bp = Blueprint("prestamos", __name__)
mediator = BibliotecaMediator()


@prestamo_bp.post("")
@requiere_rol("admin", "bibliotecario")
def crear_prestamo():
    data = request.get_json()
    try:
        prestamo = mediator.solicitar_prestamo(
            usuario_id=data.get("usuario_id"),
            libro_id=data.get("libro_id"),
            dias=data.get("dias", 7),
        )
        return jsonify(prestamo.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@prestamo_bp.post("/<int:prestamo_id>/devolucion")
@requiere_rol("admin", "bibliotecario")
def devolver_prestamo(prestamo_id):
    try:
        prestamo = mediator.registrar_devolucion(prestamo_id)
        return jsonify(prestamo.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@prestamo_bp.get("")
def listar_prestamos():
    prestamos = Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).all()
    return jsonify([p.to_dict() for p in prestamos])


@prestamo_bp.get("/usuario/<int:usuario_id>")
def historial_usuario(usuario_id):
    prestamos = Prestamo.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([p.to_dict() for p in prestamos])
