"""Crea un usuario administrador inicial. Ejecutar una sola vez:
python seed.py
"""
from app import create_app
from app.services.facade import BibliotecaFacade

app = create_app()

with app.app_context():
    facade = BibliotecaFacade()
    try:
        admin = facade.crear_usuario(
            nombre="Morgan Leonel",
            correo="morganleonel@biblioteca.com",
            password="318334792",
            tipo="admin",
        )
        print(f"Admin creado: {admin.correo} / 318334792")
    except ValueError as e:
        print(f"Aviso: {e}")
