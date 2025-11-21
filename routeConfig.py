from routes.user_routes import user_bp

def register_routes(app):
    print("[✔] Registrando rutas...")

    # Registrar rutas para usuarios
    app.register_blueprint(user_bp)

    print("[✔] Rutas registradas exitosamente")
