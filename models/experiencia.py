from config.database import db

class Experiencia(db.Model):
    __tablename__ = "experiencia"

    id_experiencia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    duracion_horas = db.Column(db.Numeric(5, 2), nullable=False)
    capacidad_maxima = db.Column(db.Integer, nullable=False)
    precio_por_persona = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())