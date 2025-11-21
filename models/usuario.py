from config.database import db

class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), nullable=False, unique=True)
    contrasena = db.Column(db.String(255), nullable=False)
    id_tipo_usuario = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
