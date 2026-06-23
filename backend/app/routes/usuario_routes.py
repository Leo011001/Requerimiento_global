from flask import Blueprint, request, jsonify
from app.services.facade import BibliotecaFacade
from app.patterns.decorators import requiere_rol

usuario_bp = Blueprint("usuarios", __name__)
facade = BibliotecaFacade()


@usuario_bp.post("")
@requiere_rol("admin")
def crear_usuario():
    data = request.get_json()
    try:
        usuario = facade.crear_usuario(
            nombre=data.get("nombre"),
            correo=data.get("correo"),
            password=data.get("password"),
            tipo=data.get("tipo", "alumno"),
        )
        return jsonify(usuario.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@usuario_bp.get("")
@requiere_rol("admin", "bibliotecario")
def listar_usuarios():
    usuarios = facade.listar_usuarios()
    return jsonify([u.to_dict() for u in usuarios])


@usuario_bp.put("/<int:usuario_id>")
@requiere_rol("admin")
def actualizar_usuario(usuario_id):
    data = request.get_json()
    try:
        usuario = facade.actualizar_usuario(usuario_id, **data)
        return jsonify(usuario.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@usuario_bp.delete("/<int:usuario_id>")
@requiere_rol("admin")
def baja_usuario(usuario_id):
    try:
        facade.dar_baja_usuario(usuario_id)
        return jsonify({"mensaje": "Usuario dado de baja"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
