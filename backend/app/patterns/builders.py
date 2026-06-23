"""
PATRÓN BUILDER:
Permite construir objetos complejos (Usuario, Prestamo) paso a paso,
validando cada campo antes de finalizar la construcción. Útil cuando
el objeto tiene varias reglas de negocio que cumplir antes de persistirse.
"""
from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.models.prestamo import Prestamo


class UsuarioBuilder:
    def __init__(self):
        self._nombre = None
        self._correo = None
        self._password = None
        self._tipo = "alumno"

    def con_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        self._nombre = nombre.strip()
        return self

    def con_correo(self, correo):
        if "@" not in correo:
            raise ValueError("Correo inválido")
        self._correo = correo.strip().lower()
        return self

    def con_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self._password = password
        return self

    def con_tipo(self, tipo):
        if tipo not in ("admin", "bibliotecario", "alumno"):
            raise ValueError("Tipo de usuario inválido")
        self._tipo = tipo
        return self

    def build(self) -> Usuario:
        if not all([self._nombre, self._correo, self._password]):
            raise ValueError("Faltan datos obligatorios para crear el usuario")
        usuario = Usuario(nombre=self._nombre, correo=self._correo, tipo=self._tipo)
        usuario.set_password(self._password)
        return usuario


class PrestamoBuilder:
    def __init__(self):
        self._usuario_id = None
        self._libro_id = None
        self._dias_prestamo = 7

    def para_usuario(self, usuario_id):
        self._usuario_id = usuario_id
        return self

    def del_libro(self, libro_id):
        self._libro_id = libro_id
        return self

    def por_dias(self, dias):
        self._dias_prestamo = dias
        return self

    def build(self) -> Prestamo:
        if not self._usuario_id or not self._libro_id:
            raise ValueError("Usuario y libro son obligatorios para el préstamo")
        return Prestamo(
            usuario_id=self._usuario_id,
            libro_id=self._libro_id,
            fecha_devolucion_esperada=datetime.utcnow() + timedelta(days=self._dias_prestamo),
        )
