# server.py

from flask import Flask
from config.database import init_db
from routeConfig import register_routes

def create_app():
    app = Flask(__name__)

    # Inicializar base de datos
    init_db(app)

    # Registrar rutas
    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
