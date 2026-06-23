from flask import Blueprint, request, jsonify
from app.services.facade import BibliotecaFacade
from app.patterns.decorators import requiere_rol

libro_bp = Blueprint("libros", __name__)
facade = BibliotecaFacade()


@libro_bp.post("")
@requiere_rol("admin", "bibliotecario")
def registrar_libro():
    data = request.get_json()
    try:
        libro = facade.registrar_libro(
            titulo=data.get("titulo"),
            autor=data.get("autor"),
            isbn=data.get("isbn"),
            categoria=data.get("categoria", ""),
            copias=data.get("copias", 1),
        )
        return jsonify(libro.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@libro_bp.get("")
def listar_libros():
    libros = facade.listar_libros()
    return jsonify([l.to_dict() for l in libros])


@libro_bp.put("/<int:libro_id>")
@requiere_rol("admin", "bibliotecario")
def actualizar_libro(libro_id):
    data = request.get_json()
    try:
        libro = facade.actualizar_libro(libro_id, **data)
        return jsonify(libro.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@libro_bp.delete("/<int:libro_id>")
@requiere_rol("admin", "bibliotecario")
def baja_libro(libro_id):
    try:
        facade.dar_baja_libro(libro_id)
        return jsonify({"mensaje": "Libro dado de baja"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
