from flask import render_template
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

def register_routes(app):
    print("[✔] Registrando rutas...")

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    @app.route('/header.html')
    def header_partial():
        return render_template('header.html')

    @app.route('/footer.html')
    def footer_partial():
        return render_template('footer.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/inicial')
    def index():
        return render_template('home.html')

    @app.route('/')
    def home():
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/contacto')
    def contacto():
        return render_template('contacto.html')

    @app.route('/editar')
    def editar():
        return render_template('editar.html')

    @app.route('/experiencias')
    def experiencias():
        return render_template('experiencias.html')

    @app.route('/perfil')
    def perfil():
        return render_template('perfil.html')

    @app.route('/publicar')
    def publicar():
        return render_template('publicar.html')

    print("[✔] Rutas registradas exitosamente")
