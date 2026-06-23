"""
PATRÓN DECORATOR:
`requiere_rol` envuelve (decora) las funciones de las rutas Flask para
añadirles, sin modificar su código interno, la responsabilidad extra de
verificar el rol del usuario autenticado antes de ejecutarse.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def requiere_rol(*roles_permitidos):
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("tipo") not in roles_permitidos:
                return jsonify({"error": "No tienes permisos para esta acción"}), 403
            return funcion(*args, **kwargs)
        return wrapper
    return decorador
