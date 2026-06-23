from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json()
    correo = data.get("correo", "").strip().lower()
    password = data.get("password", "")

    usuario = Usuario.query.filter_by(correo=correo, activo=True).first()
    if not usuario or not usuario.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"tipo": usuario.tipo, "nombre": usuario.nombre},
    )
    return jsonify({"token": token, "usuario": usuario.to_dict()})
