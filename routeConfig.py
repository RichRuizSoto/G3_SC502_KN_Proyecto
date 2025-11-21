from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from flask import render_template

def register_routes(app):
    print("[✔] Registrando rutas...")

    # Registrar API
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # Registrar rutas para header y footer
    @app.route('/header.html')
    def header_partial():
        return render_template('header.html')

    @app.route('/footer.html')
    def footer_partial():
        return render_template('footer.html')

    print("[✔] Rutas registradas exitosamente")
