from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise Exception("ERROR: No se encontró la variable DATABASE_URL en el .env")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    print("✔ Base de datos conectada correctamente a MySQL")
